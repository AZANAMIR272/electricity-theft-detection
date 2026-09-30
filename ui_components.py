"""
UI components for Streamlit interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COMPANY_NAME, LOGO_BASE64, LOGO_MIME, get_custom_css, THRESHOLD
from visualizations import (
    create_risk_gauge_chart, create_probability_gauge_chart,
    create_feature_comparison_chart, create_risk_distribution_chart,
    create_probability_histogram, create_risk_timeline_chart, create_3d_feature_plot,
    create_model_comparison_chart
)
from model_utils import calculate_feature_importance
from email_utils import send_email, generate_customer_warning_email, generate_inspection_team_email
from reports import generate_inspection_report
import datetime
import json

def setup_page():
    """Setup Streamlit page configuration and styling"""
    st.set_page_config(
        page_title=f"{COMPANY_NAME} Theft Detection",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Header with branding
    st.markdown(f"""
    <div class="header-branding">
        <img src="data:{LOGO_MIME};base64,{LOGO_BASE64}" alt="Company Logo">
        <h1>{COMPANY_NAME} Theft Detector</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Powered by Explainable Machine Learning & Advanced Analytics", unsafe_allow_html=True)
    st.caption("✨ Featuring Interactive Visualizations, Feature Importance Analysis, and Multi-Format Exports")
    st.info("**Instructions:** Upload customer data (manual entry) or batch CSV file to generate electricity theft predictions. The system provides risk levels, explanatory insights, and actionable recommendations.")

def setup_sidebar():
    """Setup sidebar navigation and email configuration"""
    st.sidebar.header("📍 Navigation")
    mode_labels = ['Manual Data Entry', 'Upload CSV File for Batch Analysis']
    mode = st.sidebar.radio("Select Prediction Mode:", mode_labels)
    actual_mode = mode
    st.sidebar.markdown("---")
    st.sidebar.success("✅ **Model Status:** Ready for Prediction")

    # Unique Features Info
    with st.sidebar.expander("🎯 Unique Features", expanded=False):
        st.markdown("""
        **📊 Advanced Analytics:**
        - Interactive Visualizations
        - Feature Importance Analysis
        - Risk Score Gauge Charts
        - 3D Feature Space Plots
        
        **💾 Data Management:**
        - Advanced Filtering & Search
        - Multi-Format Exports (CSV, Excel, JSON)
        - Automated Report Generation
        - Sortable & Filterable Tables
        """)

    # Email Configuration
    with st.sidebar.expander("📧 Email Configuration", expanded=False):
        st.markdown("**SMTP Settings:**")
        smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com", help="e.g., smtp.gmail.com, smtp.outlook.com")
        smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
        sender_email = st.text_input("Sender Email", help="Your email address")
        sender_password = st.text_input("Sender Password", type="password", help="Email password or app-specific password")
        
        st.markdown("---")
        st.markdown("**Recipient Emails:**")
        customer_email = st.text_input("Customer Warning Email", help="Email for customer warnings (Medium risk, no theft)")
        inspection_team_email = st.text_input("Inspection Team Email", help="Email for theft alerts (High/Medium risk with theft)")
        
        # Save email config to session state
        st.session_state.email_config = {
            'smtp_server': smtp_server,
            'smtp_port': int(smtp_port),
            'sender_email': sender_email,
            'sender_password': sender_password,
            'customer_email': customer_email,
            'inspection_team_email': inspection_team_email
        }
    
    return actual_mode

def display_manual_results(customer_id, final_result, manual_data, model):
    """Display results for manual entry mode"""
    risk = final_result['Risk_Level'].iloc[0]
    prob = final_result['Theft_Probability'].iloc[0]
    action = final_result['Next_Action'].iloc[0]
    risk_score = final_result['Risk_Score'].iloc[0]
    prob_raw = final_result['Theft_Probability_Raw'].iloc[0] * 100
    
    st.markdown("---")
    st.header(f"🔍 Result for {customer_id}")
    st.markdown("### 📋 Prediction Summary")
    
    # Metrics
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("⚠️ Risk Level", risk, delta_color="off")
    col_m2.metric("📊 Theft Probability", prob)
    col_m3.metric("✅ Confidence Score", f"{final_result['Confidence_Score'].iloc[0]:.1%}", delta_color="off")
    col_m4.metric("🎯 Action Required", action, delta_color="off")
    
    # Visualizations
    st.markdown("---")
    st.subheader("📊 Advanced Analytics Dashboard")
    st.caption("Interactive charts provide visual insights into customer risk assessment")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.plotly_chart(create_risk_gauge_chart(risk_score), use_container_width=True)
        st.caption("🟢 Low Risk (0-40) | 🟡 Medium Risk (40-70) | 🔴 High Risk (70-100)")
    
    with col_v2:
        st.plotly_chart(create_probability_gauge_chart(prob_raw, THRESHOLD*100), use_container_width=True)
        st.caption(f"🔴 Threshold: {THRESHOLD*100}% (Values above this are considered high risk)")
    
    model_comp_chart = create_model_comparison_chart()
    st.plotly_chart(model_comp_chart, use_container_width=True)
    st.caption("Comparison of model accuracies. This system uses the highlighted XGBoost model for its superior performance.")
    
    # Feature Importance
    try:
        feature_importance = calculate_feature_importance(manual_data.iloc[0], prob_raw/100, model)
        if feature_importance and len(feature_importance) > 0:
            st.markdown("### 🔍 Feature Contribution Analysis")
            st.caption("This chart shows which features contribute most significantly to the prediction")
            fig_importance = create_feature_comparison_chart(manual_data.iloc[0], feature_importance)
            if fig_importance:
                st.plotly_chart(fig_importance, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Feature importance calculation skipped: {str(e)}")
    
    # Feature Values Chart
    st.markdown("### 📈 Input Feature Values")
    st.caption("Detailed breakdown of customer input features")
    feature_data = manual_data.iloc[0].drop(['CONS_NO'], errors='ignore')
    fig_features = px.bar(
        x=feature_data.values,
        y=feature_data.index,
        orientation='h',
        title="Customer Feature Values",
        color=feature_data.values,
        color_continuous_scale='Blues'
    )
    fig_features.update_layout(
        height=400, showlegend=False, xaxis_title="Value", yaxis_title="Feature",
        paper_bgcolor='rgba(255,255,255,0.9)', plot_bgcolor='rgba(255,255,255,0.9)',
        font={'color': '#1a1a1a'}
    )
    st.plotly_chart(fig_features, use_container_width=True)
    
    # Explanatory Insights
    st.markdown("---")
    st.markdown("### 💡 Explanatory Insights")
    
    if risk in ['High', 'Medium']:
        st.error(f"**⚠️ Description:** {final_result['Theft_Description'].iloc[0]}")
        st.warning(f"**🎯 Next Action:** {action}")
        st.info(f"**📊 Confidence Score:** {final_result['Confidence_Score'].iloc[0]:.2%}")
        
        # Action Center
        st.markdown("---")
        st.subheader("🎯 Action Center (High/Medium Risk)")
        st.caption("Download or send reports for high-risk cases")
        
        report_text = generate_inspection_report(customer_id, final_result.iloc[0], manual_data.iloc[0])
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.download_button(
                label="⬇️ Download Report (.txt)",
                data=report_text,
                file_name=f"Report_{customer_id}_{datetime.date.today()}.txt",
                mime="text/plain"
            )
        with col_b:
            report_json = {
                'customer_id': customer_id,
                'timestamp': datetime.datetime.now().isoformat(),
                'risk_level': str(risk),
                'theft_probability': float(prob_raw),
                'risk_score': float(risk_score),
                'confidence_score': float(final_result['Confidence_Score'].iloc[0]),
                'description': final_result['Theft_Description'].iloc[0],
                'next_action': action,
                'features': manual_data.iloc[0].to_dict()
            }
            st.download_button(
                label="⬇️ Download Report (.json)",
                data=json.dumps(report_json, indent=2),
                file_name=f"Report_{customer_id}_{datetime.date.today()}.json",
                mime="application/json"
            )
        with col_c:
            pass  # Email sent automatically
    
    # Automatic Email System
    prediction_value = final_result['Prediction'].iloc[0]
    is_theft_detected = prediction_value == 1
    email_config = st.session_state.get('email_config', {})
    
    if email_config.get('sender_email') and email_config.get('sender_password'):
        # Condition 1: Medium Risk + No Theft → Send warning to customer
        if risk == 'Medium' and not is_theft_detected:
            customer_email_addr = email_config.get('customer_email', '')
            if customer_email_addr:
                try:
                    html_body, text_body = generate_customer_warning_email(customer_id, risk, prob)
                    success, message = send_email(
                        email_config['smtp_server'], email_config['smtp_port'],
                        email_config['sender_email'], email_config['sender_password'],
                        customer_email_addr,
                        f"⚠️ Electricity Consumption Warning - Customer {customer_id}",
                        html_body, text_body
                    )
                    if success:
                        st.success(f"✅ Warning email sent to customer: {customer_email_addr}")
                    else:
                        st.warning(f"⚠️ Failed to send customer email: {message}")
                except Exception as e:
                    st.warning(f"⚠️ Email error: {str(e)}")
        
        # Condition 2: High/Medium Risk + Theft Detected → Send to inspection team
        if risk in ['High', 'Medium'] and is_theft_detected:
            inspection_email_addr = email_config.get('inspection_team_email', '')
            if inspection_email_addr:
                try:
                    html_body, text_body = generate_inspection_team_email(
                        customer_id, final_result.iloc[0], manual_data.iloc[0]
                    )
                    report_attachment = report_text.encode('utf-8')
                    success, message = send_email(
                        email_config['smtp_server'], email_config['smtp_port'],
                        email_config['sender_email'], email_config['sender_password'],
                        inspection_email_addr,
                        f"🚨 URGENT: Theft Detected - Customer {customer_id}",
                        html_body, text_body,
                        attachment_data=report_attachment,
                        attachment_name=f"Report_{customer_id}_{datetime.date.today()}.txt"
                    )
                    if success:
                        st.success(f"✅ Alert email sent to inspection team: {inspection_email_addr}")
                        st.balloons()
                    else:
                        st.warning(f"⚠️ Failed to send inspection email: {message}")
                except Exception as e:
                    st.warning(f"⚠️ Email error: {str(e)}")
    else:
        st.info("ℹ️ Configure email settings in sidebar to enable automatic email notifications")
    
    if risk not in ['High', 'Medium']:
        st.success("✅ **Normal Consumption Pattern**")
        st.info(f"**📝 Description:** {final_result['Theft_Description'].iloc[0]}")
        st.info(f"**📊 Confidence Score:** {final_result['Confidence_Score'].iloc[0]:.2%}")

def process_batch_emails(final_batch_result, new_data_df, email_config):
    """Process and send emails for batch predictions"""
    customer_warnings_sent = 0
    inspection_alerts_sent = 0
    
    for idx, row in final_batch_result.iterrows():
        customer_id = idx
        risk_level = row['Risk_Level']
        is_theft = row['Prediction'] == 1
        
        # Condition 1: Medium Risk + No Theft → Send warning to customer
        if risk_level == 'Medium' and not is_theft:
            customer_email_addr = email_config.get('customer_email', '')
            if customer_email_addr:
                try:
                    html_body, text_body = generate_customer_warning_email(
                        customer_id, risk_level, row['Theft_Probability']
                    )
                    success, message = send_email(
                        email_config['smtp_server'], email_config['smtp_port'],
                        email_config['sender_email'], email_config['sender_password'],
                        customer_email_addr,
                        f"⚠️ Electricity Consumption Warning - Customer {customer_id}",
                        html_body, text_body
                    )
                    if success:
                        customer_warnings_sent += 1
                except Exception:
                    pass
        
        # Condition 2: High/Medium Risk + Theft Detected → Send to inspection team
        if risk_level in ['High', 'Medium'] and is_theft:
            inspection_email_addr = email_config.get('inspection_team_email', '')
            if inspection_email_addr:
                try:
                    original_row = new_data_df.loc[customer_id]
                    html_body, text_body = generate_inspection_team_email(customer_id, row, original_row)
                    report_text = generate_inspection_report(customer_id, row, original_row)
                    report_attachment = report_text.encode('utf-8')
                    success, message = send_email(
                        email_config['smtp_server'], email_config['smtp_port'],
                        email_config['sender_email'], email_config['sender_password'],
                        inspection_email_addr,
                        f"🚨 URGENT: Theft Detected - Customer {customer_id}",
                        html_body, text_body,
                        attachment_data=report_attachment,
                        attachment_name=f"Report_{customer_id}_{datetime.date.today()}.txt"
                    )
                    if success:
                        inspection_alerts_sent += 1
                except Exception:
                    pass
    
    return customer_warnings_sent, inspection_alerts_sent
