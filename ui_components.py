"""
UI components for Streamlit interface (High-Fidelity Claymorphism theme)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import (
    COMPANY_NAME, LOGO_BASE64, LOGO_MIME, get_custom_css, THRESHOLD,
    get_clay_blobs, clay_section_title, clay_metric, clay_chip, clay_info_card,
)
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


# =================================================================
# HELPERS
# =================================================================
def clay_container():
    """Streamlit container that our CSS renders as a floating clay card."""
    return st.container(border=True)


def load_email_secrets():
    """
    Read SMTP settings from Streamlit Secrets (.streamlit/secrets.toml).
    Used in production / cloud deployments so credentials never live in code.
    Falls back to {} when no secrets file exists (local development).
    """
    try:
        if "smtp" not in st.secrets:
            return {}
        s = st.secrets["smtp"]
        return {
            "smtp_server": str(s.get("smtp_server", "smtp.gmail.com")),
            "smtp_port": int(s.get("smtp_port", 587)),
            "sender_email": str(s.get("sender_email", "")),
            "sender_password": str(s.get("sender_password", "")),
            "customer_email": str(s.get("customer_email", "")),
            "inspection_team_email": str(s.get("inspection_team_email", "")),
        }
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


# =================================================================
# PAGE SETUP + BRANDING
# =================================================================
def setup_page():
    """Setup Streamlit page configuration, clay theme and branded hero."""
    st.set_page_config(
        page_title=f"{COMPANY_NAME} Theft Detection",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Clay design system
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    st.markdown(get_clay_blobs(), unsafe_allow_html=True)

    # --- Hero card ---
    st.markdown(f"""
    <div class="clay-hero">
      <div class="clay-hero-row">
        <img class="clay-hero-logo" src="data:{LOGO_MIME};base64,{LOGO_BASE64}" alt="{COMPANY_NAME} logo">
        <div>
          <h1>Electricity Theft Detection</h1>
          <p class="clay-hero-sub">Explainable machine learning that turns smart-meter data into
          risk levels, reasons and a ready-to-run field action.</p>
        </div>
      </div>
      <div class="clay-hero-badges">
        <span class="clay-chip clay-chip-amber"><span class="clay-chip-icon">🏆</span>1st Position — International Conference</span>
        <span class="clay-chip clay-chip-violet"><span class="clay-chip-icon">⚡</span>XGBoost 80.02% Accuracy</span>
        <span class="clay-chip clay-chip-sky"><span class="clay-chip-icon">🧠</span>Explainable AI</span>
        <span class="clay-chip clay-chip-pink"><span class="clay-chip-icon">📈</span>Interactive Analytics</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Stat orbs ---
    st.markdown(f"""
    <div class="clay-orbs">
      <div class="clay-orb">
        <span class="clay-orb-icon violet">🏆</span>
        <span class="clay-orb-value">1st</span>
        <span class="clay-orb-label">Conference Position</span>
      </div>
      <div class="clay-orb">
        <span class="clay-orb-icon pink">🎯</span>
        <span class="clay-orb-value">80.02%</span>
        <span class="clay-orb-label">Model Accuracy</span>
      </div>
      <div class="clay-orb">
        <span class="clay-orb-icon sky">🧬</span>
        <span class="clay-orb-value">9</span>
        <span class="clay-orb-label">Engineered Features</span>
      </div>
      <div class="clay-orb">
        <span class="clay-orb-icon green">⚡</span>
        <span class="clay-orb-value">2</span>
        <span class="clay-orb-label">Prediction Modes</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(clay_info_card(
        "🚀 How to use this system",
        "Pick <b>Manual Data Entry</b> for a single customer, or <b>Upload CSV File</b> for a full batch. "
        "Every prediction comes with a risk level, theft probability, confidence score, the reason behind "
        "the verdict and a recommended field action.",
        tone="violet"
    ), unsafe_allow_html=True)


# =================================================================
# SIDEBAR
# =================================================================
def setup_sidebar():
    """Setup sidebar navigation and email configuration."""
    st.sidebar.markdown(
        clay_section_title("📍 Navigation"),
        unsafe_allow_html=True
    )
    mode_labels = ['Manual Data Entry', 'Upload CSV File for Batch Analysis']
    mode = st.sidebar.radio("Select Prediction Mode:", mode_labels)
    actual_mode = mode

    st.sidebar.markdown(
        clay_chip("Model Status: Ready for Prediction", tone="green", icon="✅"),
        unsafe_allow_html=True,
    )

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

    # ---------------- Email Configuration ----------------
    secrets_cfg = load_email_secrets()

    with st.sidebar.expander("📧 Email Configuration", expanded=False):
        if secrets_cfg:
            st.markdown(clay_info_card(
                "🔐 SMTP loaded from Secrets",
                "Credentials are provided by the deployment's <code>secrets.toml</code> and are never "
                "stored in code.",
                tone="green"
            ), unsafe_allow_html=True)
            email_config = dict(secrets_cfg)
        else:
            st.markdown("**SMTP Settings:**")
            smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com",
                                         help="e.g., smtp.gmail.com, smtp.outlook.com")
            smtp_port = st.number_input("SMTP Port", value=587, min_value=1, max_value=65535)
            sender_email = st.text_input("Sender Email", help="Your email address")
            sender_password = st.text_input("Sender Password", type="password",
                                            help="Email password or app-specific password")

            st.markdown("---")
            st.markdown("**Recipient Emails:**")
            customer_email = st.text_input("Customer Warning Email",
                                           help="Email for customer warnings (Medium risk, no theft)")
            inspection_team_email = st.text_input("Inspection Team Email",
                                                  help="Email for theft alerts (High/Medium risk with theft)")

            email_config = {
                'smtp_server': smtp_server,
                'smtp_port': int(smtp_port),
                'sender_email': sender_email,
                'sender_password': sender_password,
                'customer_email': customer_email,
                'inspection_team_email': inspection_team_email
            }

        st.session_state.email_config = email_config

    return actual_mode


# =================================================================
# MANUAL MODE RESULTS
# =================================================================
def display_manual_results(customer_id, final_result, manual_data, model):
    """Display results for manual entry mode"""
    risk = final_result['Risk_Level'].iloc[0]
    prob = final_result['Theft_Probability'].iloc[0]
    action = final_result['Next_Action'].iloc[0]
    risk_score = final_result['Risk_Score'].iloc[0]
    prob_raw = final_result['Theft_Probability_Raw'].iloc[0] * 100

    tone = {'High': 'red', 'Medium': 'amber'}.get(str(risk), 'green')

    st.markdown(clay_section_title(f"🔍 Result for {customer_id}", "Live verdict from the XGBoost classifier"),
                unsafe_allow_html=True)

    # --- Metric cards ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(clay_metric("Risk Level", risk, tone=tone, icon="⚠️"), unsafe_allow_html=True)
    with m2:
        st.markdown(clay_metric("Theft Probability", prob, tone="violet", icon="📊"), unsafe_allow_html=True)
    with m3:
        st.markdown(clay_metric("Confidence Score", f"{final_result['Confidence_Score'].iloc[0]:.1%}",
                                tone="sky", icon="✅"), unsafe_allow_html=True)
    with m4:
        st.markdown(clay_metric("Action Required", action, tone="pink", icon="🎯"), unsafe_allow_html=True)

    # --- Visualizations ---
    st.markdown(clay_section_title("📊 Advanced Analytics Dashboard",
                                   "Interactive charts that visualise the customer's risk profile"),
                unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.plotly_chart(create_risk_gauge_chart(risk_score), use_container_width=True)
        st.caption("🟢 Low Risk (0-40) | 🟡 Medium Risk (40-70) | 🔴 High Risk (70-100)")

    with col_v2:
        st.plotly_chart(create_probability_gauge_chart(prob_raw, THRESHOLD * 100), use_container_width=True)
        st.caption(f"🔴 Threshold: {THRESHOLD*100}% (Values above this are considered high risk)")

    model_comp_chart = create_model_comparison_chart()
    st.plotly_chart(model_comp_chart, use_container_width=True)
    st.caption("Comparison of model accuracies. This system uses the highlighted XGBoost model for its superior performance.")

    # Feature Importance
    try:
        feature_importance = calculate_feature_importance(manual_data.iloc[0], prob_raw / 100, model)
        if feature_importance and len(feature_importance) > 0:
            st.markdown(clay_section_title("🔍 Feature Contribution Analysis",
                                           "Which features moved the prediction the most"),
                        unsafe_allow_html=True)
            fig_importance = create_feature_comparison_chart(manual_data.iloc[0], feature_importance)
            if fig_importance:
                st.plotly_chart(fig_importance, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Feature importance calculation skipped: {str(e)}")

    # Feature Values Chart
    st.markdown(clay_section_title("📈 Input Feature Values",
                                   "Detailed breakdown of the customer's input features"),
                unsafe_allow_html=True)
    feature_data = manual_data.iloc[0].drop(['CONS_NO'], errors='ignore')
    fig_features = px.bar(
        x=feature_data.values,
        y=feature_data.index,
        orientation='h',
        title="Customer Feature Values",
        color=feature_data.values,
        color_continuous_scale=['#DDD6FE', '#A78BFA', '#7C3AED']
    )
    fig_features.update_layout(
        height=400, showlegend=False, xaxis_title="Value", yaxis_title="Feature",
        paper_bgcolor='rgba(255,255,255,0)', plot_bgcolor='rgba(255,255,255,0.45)',
        font={'color': '#332F3A', 'family': 'Nunito, DM Sans, sans-serif'}
    )
    st.plotly_chart(fig_features, use_container_width=True)

    # --- Explanatory Insights ---
    st.markdown(clay_section_title("💡 Explanatory Insights",
                                   "Plain-language reasoning behind the verdict"), unsafe_allow_html=True)

    if risk in ['High', 'Medium']:
        st.error(f"**⚠️ Description:** {final_result['Theft_Description'].iloc[0]}")
        st.warning(f"**🎯 Next Action:** {action}")
        st.info(f"**📊 Confidence Score:** {final_result['Confidence_Score'].iloc[0]:.2%}")

        st.markdown(clay_section_title("🎯 Action Center",
                                       "Download or send reports for high-risk cases"), unsafe_allow_html=True)

        report_text = generate_inspection_report(customer_id, final_result.iloc[0], manual_data.iloc[0])

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.download_button(
                label="⬇️ Download Report (.txt)",
                data=report_text,
                file_name=f"Report_{customer_id}_{datetime.date.today()}.txt",
                mime="text/plain",
                type="primary"
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
