"""
Configuration file for Electricity Theft Detection System
Contains constants, CSS styling, and image loading utilities
"""

import streamlit as st
import base64

# --- Configuration Constants ---
THRESHOLD = 0.40
COMPANY_NAME = "J-ELECTRIC"
LOGO_PATH = "LOGO.jpg"
BG_IMAGE_PATH = "download.png"
MODEL_PATH = "model_theft.pkl"  # Default model path - change if needed

# --- Logo Encoding Function ---
def get_image_base64(path):
    """Encode local image file to Base64 string"""
    try:
        with open(path, "rb") as image_file:
            mime_type = "image/png" if path.lower().endswith(".png") else "image/jpeg"
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string, mime_type
    except FileNotFoundError:
        st.error(f"Error: Required file '{path}' not found.")
        st.stop()

# Logo and Background Image encoding
LOGO_BASE64, LOGO_MIME = get_image_base64(LOGO_PATH)
BG_IMAGE_BASE64, BG_MIME = get_image_base64(BG_IMAGE_PATH)

# --- Custom CSS for Branding and Background Image ---
def get_custom_css():
    """Generate custom CSS with branding"""
    return f"""
<style>
/* Background Image Setup */
.stApp {{
    background-image: url("data:{BG_MIME};base64,{BG_IMAGE_BASE64}");
    background-size: cover;
    background-attachment: fixed;
    background-repeat: no-repeat;
}}

/* Main Content Area Styling: Better contrast */
.main .block-container {{
    background-color: rgba(255, 255, 255, 0.95);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}}

/* Improved text contrast for main content */
.main h1, .main h2, .main h3, .main h4, .main p, .main label {{
    color: #1a1a1a !important;
}}

/* Sidebar Styling: Enhanced contrast */
[data-testid="stSidebar"] {{
    background-color: #1e3a5f !important;
    color: #ffffff !important;
}}

/* Sidebar Heading and Text - High Contrast White */
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] .stText {{
    color: #ffffff !important;
}}

/* Sidebar Radio buttons and inputs */
[data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stSelectbox label {{
    color: #ffffff !important;
    font-weight: 500;
}}

/* Sidebar Button - Better contrast */
[data-testid="stSidebar"] .stButton > button {{
    background-color: #e63946 !important;
    color: #ffffff !important;
    font-weight: 600;
    border: none;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background-color: #d62839 !important;
}}

/* Custom Header with Branding */
.header-branding {{
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #3366ff;
}}
.header-branding img {{
    height: 60px;
    margin-right: 15px;
}}
.header-branding h1 {{
    color: #3366ff;
    font-size: 2.5em;
    margin: 0;
}}

/* Metric Styling - Better contrast */
[data-testid="stMetric"] {{
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.12);
}}

[data-testid="stMetric"] > div {{
    color: #1a1a1a !important;
}}

[data-testid="stMetricLabel"] {{
    color: #4a5568 !important;
    font-weight: 600;
    font-size: 0.9rem;
}}

[data-testid="stMetricValue"] {{
    color: #1a202c !important;
    font-weight: 700;
    font-size: 1.8rem;
}}

/* Animation for risk indicators */
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.7; }}
}}
.risk-high {{
    animation: pulse 2s infinite;
}}

/* Enhanced card styling */
.prediction-card {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}}

/* Interactive hover effects */
.interactive-chart {{
    transition: transform 0.3s ease;
}}
.interactive-chart:hover {{
    transform: scale(1.02);
}}
</style>
"""

