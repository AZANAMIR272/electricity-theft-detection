"""
Main Streamlit Application for Electricity Theft Detection
Refactored into modular structure
"""

import streamlit as st
import pandas as pd
import datetime
import json
import warnings
import io

from config import THRESHOLD, COMPANY_NAME
from model_utils import load_model, make_prediction_and_format
from ui_components import setup_page, setup_sidebar, display_manual_results, process_batch_emails
from visualizations import (
    create_risk_distribution_chart, create_probability_histogram,
    create_risk_timeline_chart, create_3d_feature_plot,
    create_model_comparison_chart
)

warnings.filterwarnings('ignore')

# Initialize model
model = load_model()

# Setup page
setup_page()
actual_mode = setup_sidebar()

# =================================================================
# A. MANUAL ENTRY MODE 
# =================================================================
if actual_mode == 'Manual Data Entry':
    
    st.header("🔍 Single Customer Analysis")
    st.info("**Instructions:** Enter data for a single customer in the form below and check theft risk.")
    
    with st.expander("Customer Data Input Form", expanded=True):
        with st.form("manual_prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                customer_id = st.text_input("Customer ID (CONS_NO):", value="HOUSE_MANUAL")
                missing_day_count = st.number_input("Missing Day Count (missing_day_count):", min_value=0, value=10, step=1)
                avg_consumption = st.number_input("Avg Consumption (avg_consumption):", min_value=0.0, value=5.0, step=0.1)
                min_consumption = st.number_input("Min Consumption (min_consumption):", min_value=0.0, value=0.5, step=0.1)
                
            with col2:
                zero_consumption_days = st.number_input("Zero Cons Days (zero_consumption_days):", min_value=0, value=1, step=1)
                std_consumption = st.number_input("Std Consumption (std_consumption):", min_value=0.0, value=5.0, step=0.1)
                max_consumption = st.number_input("Max Consumption (max_consumption):", min_value=0.0, value=30.0, step=0.1)
                max_to_mean_ratio = st.number_input("Max to Mean Ratio (max_to_mean_ratio):", min_value=0.0, value=5.0, step=0.1)
                total_consumption = st.number_input("Total Consumption (total_consumption):", min_value=0.0, value=1500.0, step=10.0)

            manual_submitted = st.form_submit_button("⚡ Predict Theft Risk")

    if manual_submitted:
        manual_data = pd.DataFrame({
            'missing_day_count': [missing_day_count],
            'avg_consumption': [avg_consumption],
            'std_consumption': [std_consumption],
            'min_consumption': [min_consumption],
            'max_consumption': [max_consumption],
            'total_consumption': [total_consumption],
            'zero_consumption_days': [zero_consumption_days],
            'max_to_mean_ratio': [max_to_mean_ratio],
        }, index=[customer_id])
        
        final_result = make_prediction_and_format(manual_data, model)
        display_manual_results(customer_id, final_result, manual_data, model)

        with st.expander("📋 View Full Prediction Dataframe"):
            st.dataframe(final_result)


# =================================================================
# B. CSV UPLOAD MODE (Batch Analysis)
# =================================================================
elif actual_mode == 'Upload CSV File for Batch Analysis':
    
    st.header("📊 Batch Analysis (CSV Upload)")
    st.warning("⚠️ **Instructions:** CSV file must contain the same features in the same order (index: CONS_NO).")
    
    # Initialize session state for batch results
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = None
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    # Clear results if a new file is uploaded
    if uploaded_file is not None:
        current_file_name = uploaded_file.name
        if st.session_state.uploaded_file_name != current_file_name:
            st.session_state.batch_results = None
            st.session_state.uploaded_file_name = current_file_name
    else:
        st.session_state.batch_results = None
        st.session_state.uploaded_file_name = None
    
    if uploaded_file is not None:
        try:
            new_data_df = pd.read_csv(uploaded_file, index_col='CONS_NO')
            
            with st.expander("📝 View Uploaded Data Structure", expanded=False):
                st.write(f"Total {len(new_data_df)} Records Loaded.")
                st.dataframe(new_data_df.head())
            
            predict_button = st.button("🚀 Generate Batch Predictions", key='batch_predict')

            if predict_button:
                with st.spinner('🔍 Analyzing data and generating predictions...'):
                    final_batch_result = make_prediction_and_format(new_data_df, model)
                    st.session_state.batch_results = final_batch_result
                    st.session_state.uploaded_file_name = uploaded_file.name
                    
                    # Process batch emails
                    email_config = st.session_state.get('email_config', {})
                    if email_config.get('sender_email') and email_config.get('sender_password'):
                        customer_warnings_sent, inspection_alerts_sent = process_batch_emails(
                            final_batch_result, new_data_df, email_config
                        )
                        if customer_warnings_sent > 0 or inspection_alerts_sent > 0:
                            st.success(f"📧 **Emails Sent:** {customer_warnings_sent} customer warnings, {inspection_alerts_sent} inspection alerts")
            
            # Display results if they exist in session state
            if st.session_state.batch_results is not None:
                final_batch_result = st.session_state.batch_results
                
                st.markdown("---")
                st.header("📊 Batch Prediction Results")
                st.success(f"✅ **Analysis Complete:** {len(final_batch_result)} customers processed successfully")
                
                # Batch Summary Metrics
                high_risk_count = final_batch_result[final_batch_result['Risk_Level'] == 'High'].shape[0]
                medium_risk_count = final_batch_result[final_batch_result['Risk_Level'] == 'Medium'].shape[0]
                low_risk_count = final_batch_result[final_batch_result['Risk_Level'] == 'Low'].shape[0]
                total_risk = high_risk_count + medium_risk_count
                
                st.markdown("### 📈 Summary of Actionable Cases")
                col_b1, col_b2, col_b3, col_b4, col_b5 = st.columns(5)
                col_b1.metric("📋 Total Records", len(final_batch_result))
                col_b2.metric("🔴 High Risk", high_risk_count, delta=f"{high_risk_count/len(final_batch_result)*100:.1f}%", delta_color="inverse")
                col_b3.metric("🟡 Medium Risk", medium_risk_count, delta=f"{medium_risk_count/len(final_batch_result)*100:.1f}%")
                col_b4.metric("🟢 Low Risk", low_risk_count, delta=f"{low_risk_count/len(final_batch_result)*100:.1f}%", delta_color="off")
                col_b5.metric("⚠️ For Inspection", total_risk, delta=f"{total_risk/len(final_batch_result)*100:.1f}%")

                # Visualizations
                st.markdown("---")
                st.subheader("📊 Advanced Analytics Dashboard")
                st.caption("Interactive charts displaying risk distribution across all customers in the batch")
                
                viz_col1, viz_col2 = st.columns(2)
                with viz_col1:
                    risk_pie = create_risk_distribution_chart(final_batch_result)
                    st.plotly_chart(risk_pie, use_container_width=True)
                    st.caption("Risk Level Distribution")
                
                with viz_col2:
                    prob_hist = create_probability_histogram(final_batch_result)
                    st.plotly_chart(prob_hist, use_container_width=True)
                    st.caption("Theft Probability Distribution")
                
                model_comp_chart = create_model_comparison_chart()
                st.plotly_chart(model_comp_chart, use_container_width=True)
                st.caption("Comparison of model accuracies. This system uses the highlighted XGBoost model for its superior performance.")
                
                st.markdown("### 🏆 Top 20 Highest Risk Customers")
                risk_timeline = create_risk_timeline_chart(final_batch_result)
                st.plotly_chart(risk_timeline, use_container_width=True)
                
                if len(final_batch_result) >= 3:
                    with st.expander("🌐 3D Feature Space Visualization", expanded=False):
                        st.plotly_chart(create_3d_feature_plot(final_batch_result), use_container_width=True)

                # Filtering and Search
                st.markdown("---")
                st.subheader("🔍 Advanced Filtering & Search")
                st.caption("Filter results based on specific criteria")
                
                filter_col1, filter_col2, filter_col3 = st.columns(3)
                with filter_col1:
                    filter_risk = st.multiselect(
                        "Filter by Risk Level",
                        options=['Low', 'Medium', 'High'],
                        default=['Low', 'Medium', 'High']
                    )
                with filter_col2:
                    min_prob = st.slider("Min Probability (%)", 0, 100, 0)
                with filter_col3:
                    search_customer = st.text_input("🔎 Search Customer ID", "")
                
                # Apply filters
                filtered_result = final_batch_result.copy()
                if filter_risk:
                    filtered_result = filtered_result[filtered_result['Risk_Level'].isin(filter_risk)]
                if min_prob > 0:
                    filtered_result = filtered_result[filtered_result['Theft_Probability_Raw'] * 100 >= min_prob]
                if search_customer:
                    filtered_result = filtered_result[filtered_result.index.str.contains(search_customer, case=False, na=False)]
                
                st.info(f"📊 **Displaying:** {len(filtered_result)} of {len(final_batch_result)} records")

                # Explanatory Insights
                st.markdown("---")
                st.subheader("💡 Detected Explanatory Insights")
                
                theft_cases = filtered_result[filtered_result['Prediction'] == 1]
                if not theft_cases.empty:
                    top_explanations = theft_cases['Theft_Description'].value_counts().nlargest(5)
                    
                    import plotly.express as px
                    fig_expl = px.bar(
                        x=top_explanations.values,
                        y=top_explanations.index,
                        orientation='h',
                        title="Top Theft Detection Reasons",
                        color=top_explanations.values,
                        color_continuous_scale='Reds',
                        labels={'x': 'Count', 'y': 'Reason'}
                    )
                    fig_expl.update_layout(
                        height=300, showlegend=False,
                        paper_bgcolor='rgba(255,255,255,0.9)',
                        plot_bgcolor='rgba(255,255,255,0.9)',
                        font={'color': '#1a1a1a'}
                    )
                    st.plotly_chart(fig_expl, use_container_width=True)
                    
                    st.markdown("**📋 Detailed Breakdown:**")
                    st.dataframe(top_explanations.reset_index().rename(columns={'index': 'Theft Reason', 'Theft_Description': 'Count'}), hide_index=True)
                else:
                    st.info("✅ No theft cases detected in filtered results.")

                # Detailed Table with sorting
                st.markdown("---")
                st.subheader("📋 Detailed Analysis Table")
                st.caption("Sort and view data using different criteria")
                
                sort_col1, sort_col2 = st.columns(2)
                with sort_col1:
                    sort_by = st.selectbox("Sort by", ['Risk_Score', 'Theft_Probability_Raw', 'Confidence_Score', 'Index'], key='sort_by')
                with sort_col2:
                    sort_order = st.selectbox("Order", ['Descending', 'Ascending'], key='sort_order')
                
                display_result = filtered_result.sort_values(
                    by=sort_by, 
                    ascending=(sort_order == 'Ascending')
                )
                
                st.dataframe(display_result, use_container_width=True)
                
                # Export Options
                st.markdown("---")
                st.subheader("💾 Export Options")
                st.caption("Download results in multiple formats")
                
                @st.cache_data
                def convert_df_csv(df):
                    return df.to_csv().encode('utf-8')
                
                @st.cache_data
                def convert_df_excel(df):
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_to_export = df.copy()
                        cols_to_drop = ['Theft_Probability_Raw']
                        df_to_export = df_to_export.drop(columns=[c for c in cols_to_drop if c in df_to_export.columns])
                        df_to_export.to_excel(writer, sheet_name='Predictions', index=True)
                        
                        summary_data = {
                            'Metric': ['Total Records', 'High Risk', 'Medium Risk', 'Low Risk', 'Total for Inspection'],
                            'Count': [
                                len(df),
                                len(df[df['Risk_Level'] == 'High']),
                                len(df[df['Risk_Level'] == 'Medium']),
                                len(df[df['Risk_Level'] == 'Low']),
                                len(df[df['Risk_Level'].isin(['High', 'Medium'])])
                            ]
                        }
                        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                    return output.getvalue()
                
                export_col1, export_col2, export_col3 = st.columns(3)
                
                with export_col1:
                    csv_file = convert_df_csv(display_result)
                    st.download_button(
                        label="⬇️ Download as CSV",
                        data=csv_file,
                        file_name=f'theft_prediction_batch_{datetime.date.today()}.csv',
                        mime='text/csv',
                    )
                
                with export_col2:
                    try:
                        excel_file = convert_df_excel(display_result)
                        st.download_button(
                            label="⬇️ Download as Excel",
                            data=excel_file,
                            file_name=f'theft_prediction_batch_{datetime.date.today()}.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        )
                    except ImportError:
                        st.warning("⚠️ Excel export requires openpyxl. Install with: pip install openpyxl")
                    except Exception as e:
                        st.warning(f"⚠️ Excel export error: {str(e)}")
                
                with export_col3:
                    json_export = display_result.to_json(orient='records', indent=2)
                    st.download_button(
                        label="⬇️ Download as JSON",
                        data=json_export,
                        file_name=f'theft_prediction_batch_{datetime.date.today()}.json',
                        mime='application/json',
                    )
                
        except Exception as e:
            st.error(f"Error reading or processing file: {e}")
            st.warning("Please check if the CSV file has the correct column names and 'CONS_NO' as index.")
