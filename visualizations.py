"""
Visualization utilities for creating charts and graphs
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import THRESHOLD

def create_risk_distribution_chart(result_df):
    """Create interactive risk level distribution chart"""
    risk_counts = result_df['Risk_Level'].value_counts().reindex(['Low', 'Medium', 'High'], fill_value=0)
    
    colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Risk Level Distribution",
        color=risk_counts.index,
        color_discrete_map=colors,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont={'color': '#ffffff', 'size': 14})
    fig.update_layout(
        showlegend=True, 
        height=400,
        paper_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig

def create_model_comparison_chart():
    """Create a unique styled chart comparing model accuracies."""
    models_data = {
        'Model': ['XGBoost', 'Decision Tree', 'Linear Regression', 'KNN'],
        'Accuracy': [80.02, 75.76, 73.70, 71.27]
    }
    # Sort ascending for horizontal plot (bottom to top)
    model_df = pd.DataFrame(models_data).sort_values('Accuracy', ascending=True)
    
    fig = go.Figure()

    # Add horizontal lines (sticks)
    for i, row in model_df.iterrows():
        color = '#ef4444' if row['Model'] == 'XGBoost' else '#cbd5e1'
        width = 3 if row['Model'] == 'XGBoost' else 2
        
        fig.add_trace(go.Scatter(
            x=[0, row['Accuracy']],
            y=[row['Model'], row['Model']],
            mode='lines',
            line=dict(color=color, width=width),
            hoverinfo='skip',
            showlegend=False
        ))

    # Add markers (lollipops)
    colors = ['#ef4444' if m == 'XGBoost' else '#94a3b8' for m in model_df['Model']]
    
    fig.add_trace(go.Scatter(
        x=model_df['Accuracy'],
        y=model_df['Model'],
        mode='markers+text',
        marker=dict(
            color=colors,
            size=30,
            line=dict(color='white', width=2),
            symbol='circle'
        ),
        text=[f"{acc:.1f}" for acc in model_df['Accuracy']],
        textposition="middle center",
        textfont=dict(color='white', size=11, family="Arial, sans-serif", weight='bold'),
        hoverinfo='x+y',
        name='Accuracy'
    ))

    fig.update_layout(
        title=dict(
            text="<b>🏆 Model Accuracy Leaderboard</b>",
            font=dict(size=18, color='#1a1a1a'),
            x=0,
            y=0.95
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            range=[0, 100],
            title="Accuracy (%)",
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            tickfont=dict(size=13, color='#1a1a1a', weight='bold')
        ),
        paper_bgcolor='rgba(255,255,255,0)',
        plot_bgcolor='rgba(255,255,255,0.5)',
        height=350,
        margin=dict(l=0, r=20, t=50, b=20),
        showlegend=False
    )
    
    # Add an annotation to highlight the used model
    xg_data = model_df[model_df['Model'] == 'XGBoost'].iloc[0]
    fig.add_annotation(
        x=xg_data['Accuracy'],
        y='XGBoost',
        text="Selected Model",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-45,
        font=dict(color='#ef4444', size=12, weight='bold'),
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#ef4444',
        borderpad=4
    )
    
    return fig

def create_probability_histogram(result_df):
    """Create histogram of theft probabilities"""
    prob_values = result_df['Theft_Probability_Raw'] * 100
    fig = px.histogram(
        x=prob_values,
        nbins=30,
        title="Theft Probability Distribution",
        labels={'x': 'Theft Probability (%)', 'y': 'Number of Customers'},
        color_discrete_sequence=['#3b82f6']
    )
    fig.add_vline(x=THRESHOLD*100, line_dash="dash", line_color="#dc2626", line_width=3,
                  annotation_text=f"Threshold: {THRESHOLD*100}%", annotation_font_size=12, annotation_font_color="#dc2626")
    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig

def create_feature_comparison_chart(row_data, feature_importance):
    """Create bar chart showing feature importance"""
    if not feature_importance:
        return None
    
    df_imp = pd.DataFrame({
        'Feature': list(feature_importance.keys()),
        'Importance (%)': list(feature_importance.values())
    }).sort_values('Importance (%)', ascending=True)
    
    fig = px.bar(
        df_imp,
        x='Importance (%)',
        y='Feature',
        orientation='h',
        title="Feature Contribution to Prediction",
        color='Importance (%)',
        color_continuous_scale='Reds',
        labels={'Importance (%)': 'Importance (%)', 'Feature': 'Feature'}
    )
    fig.update_layout(
        height=400, 
        showlegend=False,
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig

def create_risk_timeline_chart(result_df):
    """Create timeline/ranking chart for risk scores"""
    top_risky = result_df.nlargest(20, 'Risk_Score')
    
    fig = px.bar(
        top_risky.reset_index(),
        x='Risk_Score',
        y='CONS_NO',
        orientation='h',
        title="Top 20 Highest Risk Customers",
        color='Risk_Score',
        color_continuous_scale='Reds',
        labels={'CONS_NO': 'Customer ID', 'Risk_Score': 'Risk Score'}
    )
    fig.update_layout(
        height=600, 
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor='rgba(255,255,255,0.9)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig

def create_3d_feature_plot(result_df):
    """Create 3D scatter plot of key features"""
    if len(result_df) < 2:
        return None
    
    # Check if required columns exist
    required_cols = ['avg_consumption', 'std_consumption', 'zero_consumption_days', 'Risk_Score']
    available_cols = [col for col in required_cols if col in result_df.columns]
    
    if len(available_cols) < 3:
        return None
    
    try:
        plot_df = result_df.reset_index()
        # Determine hover column name
        hover_col = None
        if 'CONS_NO' in plot_df.columns:
            hover_col = 'CONS_NO'
        elif plot_df.index.name and plot_df.index.name in plot_df.columns:
            hover_col = plot_df.index.name
        elif len(plot_df) > 0:
            id_cols = [col for col in plot_df.columns if 'id' in col.lower() or 'cons' in col.lower()]
            if id_cols:
                hover_col = id_cols[0]
        
        fig = px.scatter_3d(
            plot_df,
            x='avg_consumption',
            y='std_consumption',
            z='zero_consumption_days',
            color='Risk_Score',
            size='Risk_Score',
            hover_name=hover_col,
            title="3D Feature Space Visualization",
            color_continuous_scale='RdYlGn_r',
            labels={
                'avg_consumption': 'Avg Consumption',
                'std_consumption': 'Std Consumption',
                'zero_consumption_days': 'Zero Days'
            }
        )
        fig.update_layout(
            height=600,
            paper_bgcolor='rgba(255,255,255,0.9)',
            font={'color': '#1a1a1a'}
        )
        return fig
    except Exception:
        return None

def create_risk_gauge_chart(risk_score):
    """Create risk score gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score", 'font': {'size': 18, 'color': '#1a1a1a'}},
        delta = {'reference': 50, 'font': {'color': '#1a1a1a'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': '#1a1a1a', 'tickfont': {'color': '#1a1a1a'}},
            'bar': {'color': "#dc2626" if risk_score > 70 else "#f59e0b" if risk_score > 40 else "#10b981"},
            'steps': [
                {'range': [0, 40], 'color': "#d1fae5"},
                {'range': [40, 70], 'color': "#fef3c7"},
                {'range': [70, 100], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 4},
                'thickness': 0.85,
                'value': 70
            }
        }
    ))
    fig.update_layout(
        height=300, 
        paper_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig

def create_probability_gauge_chart(prob_raw, threshold):
    """Create probability gauge chart"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prob_raw,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Theft Probability (%)", 'font': {'size': 18, 'color': '#1a1a1a'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': '#1a1a1a', 'tickfont': {'color': '#1a1a1a'}},
            'bar': {'color': "#dc2626" if prob_raw > threshold else "#10b981"},
            'steps': [
                {'range': [0, 30], 'color': "#d1fae5"},
                {'range': [30, 60], 'color': "#fef3c7"},
                {'range': [60, 100], 'color': "#fee2e2"}
            ],
            'threshold': {
                'line': {'color': "#dc2626", 'width': 4},
                'thickness': 0.85,
                'value': threshold
            }
        }
    ))
    fig.update_layout(
        height=300,
        paper_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    return fig
