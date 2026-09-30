"""
Model utilities for loading and making predictions
"""

import streamlit as st
import pandas as pd
import joblib
import numpy as np
from config import THRESHOLD, MODEL_PATH

# --- Model Loading ---
@st.cache_resource 
def load_model(model_path=None):
    if model_path is None:
        model_path = MODEL_PATH
    """Load the trained XGBoost model"""
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        st.error(f"ERROR: Model file '{model_path}' not found. Please check file name and location.")
        st.stop()

# --- Advanced Feature Importance Calculation ---
def calculate_feature_importance(row_data, base_prob, model):
    """Calculate relative importance of each feature in prediction"""
    feature_contributions = {}
    original_values = row_data.to_dict() if hasattr(row_data, 'to_dict') else dict(row_data)
    
    # Get feature names, excluding metadata columns
    exclude_cols = ['CONS_NO', 'Prediction', 'Theft_Probability', 'Theft_Probability_Raw', 
                   'Risk_Level', 'Risk_Score', 'Confidence_Score', 'Theft_Description', 'Next_Action']
    feature_names = [f for f in original_values.keys() if f not in exclude_cols]
    
    for feature in feature_names:
        temp_values = original_values.copy()
        original_val = temp_values.get(feature, 0)
        if original_val == 0:
            temp_values[feature] = 1.0
        else:
            temp_values[feature] = original_val * 1.5
        try:
            temp_df = pd.DataFrame([temp_values])
            temp_prob = model.predict_proba(temp_df[feature_names])[0, 1]
            contribution = abs(temp_prob - base_prob)
            feature_contributions[feature] = contribution
        except Exception:
            feature_contributions[feature] = 0
    
    # Normalize contributions
    total = sum(feature_contributions.values())
    if total > 0:
        feature_contributions = {k: v/total * 100 for k, v in feature_contributions.items()}
    
    return feature_contributions

# --- Prediction and Formatting Function ---
def make_prediction_and_format(data_df, model):
    """
    Make predictions on dataframe and format results with unique features
    """
    prob_array = model.predict_proba(data_df)[:, 1]
    prediction_array = (prob_array >= THRESHOLD).astype(int)

    result = data_df.copy()
    result['Theft_Probability_Raw'] = prob_array
    result['Theft_Probability'] = prob_array
    result['Prediction'] = prediction_array
    
    # Calculate confidence score (distance from threshold)
    result['Confidence_Score'] = abs(prob_array - THRESHOLD) * 2

    result['Risk_Level'] = pd.cut(
        result['Theft_Probability'],
        bins=[0, 0.3, 0.4, 1.0],
        labels=['Low', 'Medium', 'High'],
        right=False
    )
    
    # Heuristics for Explanation
    explanations = []
    next_actions = []
    risk_scores = []
    
    for index, row in result.iterrows():
        is_theft = row['Prediction'] == 1
        prob = row['Theft_Probability']
        risk_score = 0
        
        if is_theft:
            if row.get('zero_consumption_days', 0) > 50:
                explanations.append("High Zero Days Count - Possible Meter Bypass/Tampering")
                next_actions.append("IMMEDIATE FIELD INSPECTION")
                risk_score = 95
            elif row.get('std_consumption', 0) < 1.5 and row.get('avg_consumption', 0) > 2.0:
                explanations.append("Very Low Std Dev - Unnatural Constant Consumption Pattern")
                next_actions.append("IMMEDIATE FIELD INSPECTION")
                risk_score = 90
            elif row.get('max_to_mean_ratio', 0) > 10.0:
                explanations.append("Extreme Max/Mean Ratio - Consumption Spikes/Manipulation")
                next_actions.append("Remote Data Audit & Scheduled Physical Check")
                risk_score = 75
            else:
                explanations.append("Theft Detected - Pattern Unclear (Investigate Other Factors)")
                next_actions.append("Remote Data Audit & Scheduled Physical Check")
                risk_score = 65
        else:
            explanations.append("Normal Pattern (No Theft Risk)")
            next_actions.append("Monitor Next Reading Cycle")
            risk_score = 10 + (prob * 20)
        
        risk_scores.append(risk_score)
            
    result['Theft_Description'] = explanations
    result['Next_Action'] = next_actions
    result['Risk_Score'] = risk_scores
    result['Theft_Probability'] = (result['Theft_Probability'] * 100).map('{:.2f}%'.format)
    
    final_cols = list(data_df.columns) + ['Theft_Probability', 'Theft_Probability_Raw', 'Prediction', 
                                          'Risk_Level', 'Risk_Score', 'Confidence_Score', 
                                          'Theft_Description', 'Next_Action']
    return result[final_cols]

