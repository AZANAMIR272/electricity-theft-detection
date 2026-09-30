"""
Configuration & Design System for Electricity Theft Detection System

High-Fidelity Claymorphism design system ("Digital Clay").
Contains design tokens, image utilities and the full CSS theme that is
injected into the Streamlit app via ui_components.setup_page().
"""

import streamlit as st
import base64

# --- Configuration Constants ---
THRESHOLD = 0.40
COMPANY_NAME = "J-ELECTRIC"
LOGO_PATH = "LOGO.jpg"
MODEL_PATH = "model_theft.pkl"  # Default model path - change if needed

# --- Design Tokens (High-Fidelity Claymorphism) ---
CLAY = {
    "canvas": "#F4F1FA",       # Very pale, cool lavender-white
    "foreground": "#332F3A",   # Soft Charcoal (WCAG AA)
    "muted": "#635F69",        # Dark Lavender-Gray (min readable grey)
    "accent": "#7C3AED",       # Vivid Violet  (primary)
    "accent_light": "#A78BFA", # Lighter violet (gradient start)
    "accent_alt": "#DB2777",   # Hot Pink (secondary)
    "info": "#0EA5E9",         # Sky Blue
    "success": "#10B981",      # Emerald Green
    "warning": "#F59E0B",      # Amber
    "danger": "#EF4444",       # Red
    "card_bg": "rgba(255, 255, 255, 0.62)",
    "pressed_bg": "#EFEBF5",
}

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


# Logo encoding (branding header)
LOGO_BASE64, LOGO_MIME = get_image_base64(LOGO_PATH)


# =================================================================
# CLAY THEME: HTML PARTS (blobs + helper classes used by ui_components)
# =================================================================
def get_clay_blobs():
    """Floating 3D background blobs (spec: never use a flat background)."""
    return """
<div class="clay-blobs" aria-hidden="true">
  <span class="clay-blob clay-blob-violet"></span>
  <span class="clay-blob clay-blob-pink animation-delay-2000"></span>
  <span class="clay-blob clay-blob-sky animation-delay-4000"></span>
  <span class="clay-blob clay-blob-emerald animation-delay-2000"></span>
</div>
"""


def clay_section_title(title, subtitle=None):
    """Section title rendered as a clay heading block."""
    sub = f'<p class="clay-section-sub">{subtitle}</p>' if subtitle else ""
    return f"""
<div class="clay-section-title">
  <h2>{title}</h2>
  {sub}
</div>
"""


def clay_badge(text, tone="violet"):
    """Small rounded-full badge pill."""
    return f'<span class="clay-badge clay-badge-{tone}">{text}</span>'


def clay_metric(label, value, tone="violet", delta=None, icon=""):
    """
    Clay stat card replacement for st.metric.
    tone: violet | green | amber | red | sky | pink
    """
    delta_html = f'<span class="clay-metric-delta">{delta}</span>' if delta else ""
    icon_html = f'<span class="clay-metric-icon">{icon}</span>' if icon else ""
    return f"""
<div class="clay-metric clay-metric-{tone}">
  {icon_html}
  <div class="clay-metric-body">
    <span class="clay-metric-label">{label}</span>
    <span class="clay-metric-value">{value}</span>
    {delta_html}
  </div>
</div>
"""


def clay_chip(text, tone="violet", icon=""):
    """Inline chip / pill (used for hero badges & status)."""
    icon_html = f'<span class="clay-chip-icon">{icon}</span>' if icon else ""
    return f'<span class="clay-chip clay-chip-{tone}">{icon_html}{text}</span>'


def clay_info_card(title, body, tone="violet"):
    """Soft clay instruction / info card."""
    return f"""
<div class="clay-info clay-info-{tone}">
  <div class="clay-info-title">{title}</div>
  <div class="clay-info-body">{body}</div>
</div>
"""


# =================================================================
# FULL CLAY STYLESHEET
# =================================================================
def get_custom_css():
    """Generate the complete High-Fidelity Claymorphism stylesheet."""
    return _CLAY_CSS


_CLAY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Nunito:wght@600;700;800;900&display=swap');

/* ==========================================================
   1. DESIGN TOKENS
   ========================================================== */
:root {
  --clay-canvas: #F4F1FA;
  --clay-foreground: #332F3A;
  --clay-muted: #635F69;
  --clay-accent: #7C3AED;
  --clay-accent-light: #A78BFA;
  --clay-accent-alt: #DB2777;
  --clay-info: #0EA5E9;
  --clay-success: #10B981;
  --clay-warning: #F59E0B;
  --clay-danger: #EF4444;
  --clay-card-bg: rgba(255, 255, 255, 0.62);
  --clay-pressed-bg: #EFEBF5;

  --r-xl: 48px;
  --r-lg: 32px;
  --r-md: 24px;
  --r-sm: 20px;

  --clay-deep: 30px 30px 60px #cdc6d9, -30px -30px 60px #ffffff,
               inset 10px 10px 20px rgba(139, 92, 246, 0.05),
               inset -10px -10px 20px rgba(255, 255, 255, 0.8);
  --clay-card: 16px 16px 32px rgba(160, 150, 180, 0.20),
               -10px -10px 24px rgba(255, 255, 255, 0.90),
               inset 6px 6px 12px rgba(139, 92, 246, 0.03),
               inset -6px -6px 12px rgba(255, 255, 255, 1);
  --clay-card-lift: 22px 22px 44px rgba(150, 138, 178, 0.28),
                    -12px -12px 28px rgba(255, 255, 255, 0.95),
                    inset 6px 6px 12px rgba(139, 92, 246, 0.05),
                    inset -6px -6px 12px rgba(255, 255, 255, 1);
  --clay-btn: 12px 12px 24px rgba(139, 92, 246, 0.30),
              -8px -8px 16px rgba(255, 255, 255, 0.40),
              inset 4px 4px 8px rgba(255, 255, 255, 0.40),
              inset -4px -4px 8px rgba(0, 0, 0, 0.10);
  --clay-btn-hover: 16px 16px 32px rgba(139, 92, 246, 0.40),
                    -10px -10px 20px rgba(255, 255, 255, 0.60),
                    inset 4px 4px 8px rgba(255, 255, 255, 0.45),
                    inset -4px -4px 8px rgba(0, 0, 0, 0.10);
  --clay-pressed: inset 10px 10px 20px #d9d4e3, inset -10px -10px 20px #ffffff;
}

/* ==========================================================
   2. BASE
   ========================================================== */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--clay-canvas) !important;
}

body, [data-testid="stAppViewContainer"] .main,
.stApp {
  font-family: 'DM Sans', system-ui, sans-serif !important;
  color: var(--clay-foreground);
}

::selection {
  background: rgba(124, 58, 237, 0.25);
  color: var(--clay-foreground);
}

/* Scrollbars */
::-webkit-scrollbar { width: 12px; height: 12px; }
::-webkit-scrollbar-track { background: #ECE7F6; border-radius: 20px; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--clay-accent-light), var(--clay-accent));
  border-radius: 20px;
  border: 3px solid #ECE7F6;
}
::-webkit-scrollbar-thumb:hover { background: var(--clay-accent); }

/* Keyboard focus */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.30) !important;
  border-radius: var(--r-sm);
}

/* ==========================================================
   3. FLOATING BACKGROUND BLOBS
   ========================================================== */
.clay-blobs {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}
.clay-blob {
  position: absolute;
  display: block;
  width: 60vh;
  height: 60vh;
  border-radius: 9999px;
  filter: blur(70px);
  opacity: 0.85;
}
.clay-blob-violet  { background: rgba(139, 92, 246, 0.16); top: -12%; left: -10%; animation: clay-float 8s ease-in-out infinite; }
.clay-blob-pink    { background: rgba(236, 72, 153, 0.14); top: 18%; right: -14%; animation: clay-float-delayed 10s ease-in-out infinite; }
.clay-blob-sky     { background: rgba(14, 165, 233, 0.13); bottom: -18%; left: 8%;  animation: clay-float-delayed 10s ease-in-out infinite; }
.clay-blob-emerald { background: rgba(16, 185, 129, 0.12); bottom: -10%; right: -8%; animation: clay-float 8s ease-in-out infinite; }

.clay-blobs + * { position: relative; }
[data-testid="stAppViewContainer"] .main { position: relative; z-index: 1; }

.animation-delay-2000 { animation-delay: 2s !important; }
.animation-delay-4000 { animation-delay: 4s !important; }

/* ==========================================================
   4. LAYOUT: MAIN CONTAINER + SIDEBAR
   ========================================================== */
section.main .block-container,
[data-testid="stMainBlockContainer"] {
  max-width: 1240px;
  padding-top: 2.5rem;
  padding-bottom: 4rem;
  background-color: var(--clay-card-bg);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: var(--r-xl);
  box-shadow: var(--clay-card);
}

[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.58);
  backdrop-filter: blur(26px);
  -webkit-backdrop-filter: blur(26px);
  border-right: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 14px 0 40px rgba(160, 150, 180, 0.22);
}
[data-testid="stSidebar"] > div {
  padding-top: 1.6rem;
  padding-left: 1.4rem;
  padding-right: 1.4rem;
}
[data-testid="stSidebarContent"] { padding-bottom: 2rem; }

/* Sidebar headings & text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-foreground) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li {
  color: var(--clay-muted) !important;
}
[data-testid="stSidebar"] hr {
  border: 0;
  height: 2px;
  background: linear-gradient(90deg, rgba(124,58,237,.35), rgba(219,39,119,.20), transparent);
  margin: 1.2rem 0;
}

/* ==========================================================
   5. TYPOGRAPHY
   ========================================================== */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stHeader"] h1,
[data-testid="stHeader"] h2 {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-foreground) !important;
  letter-spacing: -0.02em;
  line-height: 1.15;
}
[data-testid="stMarkdownContainer"] h1 { font-weight: 900 !important; font-size: 2.4rem; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.85rem; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.4rem; }

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
  color: var(--clay-foreground);
  line-height: 1.65;
}
[data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"] small {
  color: var(--clay-muted) !important;
  font-weight: 500;
}

a { color: var(--clay-accent) !important; font-weight: 700; text-decoration: none; }
a:hover { color: var(--clay-accent-alt) !important; }

/* Section title block (clay_section_title) */
.clay-section-title { margin: 2.2rem 0 1.1rem 0; }
.clay-section-title h2 {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900 !important;
  font-size: 1.7rem !important;
  color: var(--clay-foreground) !important;
  margin: 0 !important;
  padding-bottom: 0.55rem;
  border-bottom: 4px solid transparent;
  border-image: linear-gradient(90deg, var(--clay-accent-light), var(--clay-accent-alt), rgba(14,165,233,0.5)) 1;
  display: inline-block;
}
.clay-section-sub {
  color: var(--clay-muted) !important;
  font-size: 0.95rem;
  margin: 0.5rem 0 0 0 !important;
}

/* ==========================================================
   6. BUTTONS (CLAY BUTTON - high convexity)
   ========================================================== */
.stButton, .stDownloadButton, .stFormSubmitButton { font-family: 'Nunito', sans-serif; }

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button,
[data-testid="stBaseButton"],
[data-testid="stDownloadButton"] button,
[data-testid="stFormSubmitButton"] button {
  width: 100%;
  min-height: 3rem;
  height: 3rem;
  padding: 0 1.5rem;
  border: none !important;
  border-radius: var(--r-sm) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 0.95rem;
  letter-spacing: 0.02em;
  color: var(--clay-foreground) !important;
  background: #ffffff !important;
  box-shadow: var(--clay-card) !important;
  transition: transform .2s ease, box-shadow .2s ease, background .2s ease !important;
  cursor: pointer;
}

/* Hover: lift up like it floats closer */
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stFormSubmitButton"] button:hover {
  transform: translateY(-4px);
  box-shadow: var(--clay-card-lift) !important;
}

/* Active: squish (scale .92 + pressed shadow) */
.stButton > button:active,
.stDownloadButton > button:active,
.stFormSubmitButton > button:active,
[data-testid="stDownloadButton"] button:active,
[data-testid="stFormSubmitButton"] button:active {
  transform: scale(0.92) !important;
  box-shadow: var(--clay-pressed) !important;
}

/* Primary / gradient variant */
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"],
.stDownloadButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] button[kind="primary"] {
  background: linear-gradient(135deg, var(--clay-accent-light) 0%, var(--clay-accent) 100%) !important;
  color: #ffffff !important;
  box-shadow: var(--clay-btn) !important;
}
.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
  box-shadow: var(--clay-btn-hover) !important;
  transform: translateY(-4px);
}
.stButton > button[kind="primary"]:active,
[data-testid="stBaseButton-primary"]:active {
  transform: scale(0.92) !important;
  box-shadow: var(--clay-pressed) !important;
}

/* Secondary outline variant */
.stButton > button[kind="secondary"],
[data-testid="stBaseButton-secondary"] {
  background: linear-gradient(135deg, #ffffff, #f7f4ff) !important;
  box-shadow: var(--clay-btn) !important;
}

/* Small ghost buttons keep their size */
.stButton > button[kind="borderless"],
[data-testid="stBaseButton-borderless"] {
  background: transparent !important;
  box-shadow: none !important;
  min-height: 2.4rem;
  height: 2.4rem;
}
.stButton > button[kind="borderless"]:hover { background: rgba(124,58,237,0.10) !important; transform: translateY(-2px); }

/* ==========================================================
   7. INPUTS (RECESSED CLAY)
   ========================================================== */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-baseweb="base-input"] {
  background-color: var(--clay-pressed-bg) !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  box-shadow: var(--clay-pressed) !important;
  color: var(--clay-foreground) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 1.02rem;
  min-height: 3.1rem;
  padding: 0.75rem 1.3rem !important;
  transition: background .2s ease, box-shadow .2s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-baseweb="base-input"]:focus {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.20), var(--clay-card) !important;
}
input::placeholder, textarea::placeholder { color: var(--clay-muted) !important; opacity: 0.85; }

/* Select / multiselect shells */
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stMultiselect"] [data-baseweb="select"],
[data-baseweb="select"] > div {
  background-color: var(--clay-pressed-bg) !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  box-shadow: var(--clay-pressed) !important;
  min-height: 3.1rem;
}
[data-testid="stSelectbox"] [data-baseweb="select"]:focus-within,
[data-testid="stMultiselect"] [data-baseweb="select"]:focus-within {
  background-color: #ffffff !important;
  box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.20), var(--clay-card) !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stMultiselect"] label,
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSlider"] label {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-foreground) !important;
}

/* Multiselect chips */
[data-testid="stMultiselect"] [data-baseweb="tag"] {
  background: linear-gradient(135deg, var(--clay-accent-light), var(--clay-accent)) !important;
  color: #fff !important;
  border-radius: 9999px !important;
  font-family: 'Nunito', sans-serif;
  font-weight: 700;
  box-shadow: 0 4px 10px rgba(139, 92, 246, 0.30);
}

/* Dropdown menu */
[data-baseweb="menu"] { border-radius: var(--r-md) !important; box-shadow: var(--clay-card-lift) !important; overflow: hidden; }
[data-baseweb="menu"] li {
  border-radius: var(--r-sm) !important;
  margin: 4px 8px;
  color: var(--clay-foreground) !important;
  font-family: 'DM Sans', sans-serif;
}
[data-baseweb="menu"] li:hover, [data-baseweb="menu"] li[aria-selected="true"] {
  background: linear-gradient(135deg, rgba(167,139,250,0.30), rgba(124,58,237,0.22)) !important;
  color: var(--clay-accent) !important;
  font-weight: 700;
}

/* Number input steppers */
[data-testid="stNumberInput"] [data-testid="stWidgetLabel"] ~ div button,
.stNumberInput button {
  background: #ffffff !important;
  border: none !important;
  border-radius: 9999px !important;
  box-shadow: var(--clay-card) !important;
  color: var(--clay-accent) !important;
  transition: transform .2s ease !important;
}
.stNumberInput button:hover { transform: scale(1.08); }

/* Slider */
[data-baseweb="slider"] { border-radius: var(--r-sm); }
[data-baseweb="slider"] div[data-testid="stThumbValue"] {
  background: var(--clay-accent) !important;
  border-radius: 9999px !important;
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
}
[data-baseweb="slider"] [data-baseweb="track"] { background: #E4DEF2 !important; }
[data-baseweb="slider"] [data-baseweb="handle"] {
  background: linear-gradient(135deg, var(--clay-accent-light), var(--clay-accent)) !important;
  box-shadow: 0 6px 14px rgba(139, 92, 246, 0.45) !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
  background: var(--clay-pressed-bg) !important;
  border: 2px dashed rgba(124, 58, 237, 0.35) !important;
  border-radius: var(--r-lg) !important;
  box-shadow: var(--clay-pressed) !important;
  padding: 1.6rem !important;
  transition: border-color .2s ease, background .2s ease;
}
[data-testid="stFileUploader"] section:hover {
  border-color: var(--clay-accent) !important;
  background: #ffffff !important;
}
[data-testid="stFileUploader"] label {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-accent) !important;
}

/* ==========================================================
   8. STAT CARDS (clay_metric) + st.metric
   ========================================================== */
.clay-metric {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 1.15rem 1.3rem;
  border-radius: var(--r-md);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(18px);
  box-shadow: var(--clay-card);
  transition: transform .35s ease, box-shadow .35s ease;
  overflow: hidden;
  height: 100%;
}
.clay-metric:hover { transform: translateY(-6px); box-shadow: var(--clay-card-lift); }
.clay-metric::before {
  content: "";
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 7px;
  background: var(--clay-accent);
}
.clay-metric-violet::before { background: linear-gradient(180deg, var(--clay-accent-light), var(--clay-accent)); }
.clay-metric-green::before  { background: linear-gradient(180deg, #6ee7b7, var(--clay-success)); }
.clay-metric-amber::before  { background: linear-gradient(180deg, #fcd34d, var(--clay-warning)); }
.clay-metric-red::before    { background: linear-gradient(180deg, #fca5a5, var(--clay-danger)); }
.clay-metric-sky::before    { background: linear-gradient(180deg, #7dd3fc, var(--clay-info)); }
.clay-metric-pink::before   { background: linear-gradient(180deg, #f9a8d4, var(--clay-accent-alt)); }

.clay-metric-body { display: flex; flex-direction: column; gap: 0.15rem; min-width: 0; }
.clay-metric-label {
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 0.74rem;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--clay-muted);
}
.clay-metric-value {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 1.75rem;
  line-height: 1.1;
  color: var(--clay-foreground);
  word-break: break-word;
}
.clay-metric-green .clay-metric-value { color: var(--clay-success); }
.clay-metric-amber .clay-metric-value { color: #b45309; }
.clay-metric-red .clay-metric-value   { color: #dc2626; }
.clay-metric-sky .clay-metric-value   { color: #0369a1; }
.clay-metric-pink .clay-metric-value  { color: var(--clay-accent-alt); }
.clay-metric-violet .clay-metric-value{ color: var(--clay-accent); }

.clay-metric-delta {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--clay-muted);
}
.clay-metric-icon { font-size: 1.6rem; }

/* Native st.metric restyle */
[data-testid="stMetric"] {
  background: rgba(255, 255, 255, 0.85) !important;
  border: none !important;
  border-radius: var(--r-md) !important;
  padding: 1.2rem 1.35rem !important;
  box-shadow: var(--clay-card) !important;
  transition: transform .35s ease, box-shadow .35s ease;
}
[data-testid="stMetric"]:hover { transform: translateY(-6px); box-shadow: var(--clay-card-lift); }
[data-testid="stMetricLabel"] {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-muted) !important;
  letter-spacing: 0.06em;
}
[data-testid="stMetricValue"] {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900 !important;
  color: var(--clay-foreground) !important;
}

/* ==========================================================
   9. ALERTS / MESSAGES
   ========================================================== */
[data-testid="stAlert"], [data-testid="stNotification"] {
  border: none !important;
  border-radius: var(--r-sm) !important;
  box-shadow: var(--clay-card) !important;
  background: rgba(255, 255, 255, 0.90) !important;
  color: var(--clay-foreground) !important;
  padding: 1rem 1.2rem !important;
  font-weight: 500;
}
[data-testid="stAlert"] > div, [data-testid="stAlert"] p { color: var(--clay-foreground) !important; }
[data-testid="stAlert"] svg { flex-shrink: 0; }

[data-testid="stAlert"][data-kind="info"]    { background: rgba(239, 246, 255, 0.95) !important; box-shadow: var(--clay-card), inset 5px 0 0 var(--clay-info) !important; }
[data-testid="stAlert"][data-kind="success"] { background: rgba(236, 253, 245, 0.95) !important; box-shadow: var(--clay-card), inset 5px 0 0 var(--clay-success) !important; }
[data-testid="stAlert"][data-kind="warning"] { background: rgba(255, 251, 235, 0.95) !important; box-shadow: var(--clay-card), inset 5px 0 0 var(--clay-warning) !important; }
[data-testid="stAlert"][data-kind="error"]   { background: rgba(254, 242, 242, 0.95) !important; box-shadow: var(--clay-card), inset 5px 0 0 var(--clay-danger) !important; }

/* Custom clay info card */
.clay-info {
  border-radius: var(--r-md);
  padding: 1.15rem 1.4rem;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: var(--clay-card);
  margin: 0.6rem 0 1.2rem 0;
}
.clay-info-title {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 1.02rem;
  color: var(--clay-accent);
  margin-bottom: 0.3rem;
}
.clay-info-body { color: var(--clay-foreground); line-height: 1.6; font-size: 0.97rem; }
.clay-info-green .clay-info-title { color: var(--clay-success); }
.clay-info-amber .clay-info-title { color: #b45309; }
.clay-info-red .clay-info-title   { color: #dc2626; }

/* ==========================================================
   10. CHIPS & BADGES
   ========================================================== */
.clay-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 1.05rem;
  border-radius: 9999px;
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 0.86rem;
  background: #ffffff;
  color: var(--clay-foreground);
  box-shadow: var(--clay-card);
  transition: transform .3s ease, box-shadow .3s ease;
}
.clay-chip:hover { transform: translateY(-4px); box-shadow: var(--clay-card-lift); }
.clay-chip-violet { background: linear-gradient(135deg, #ede9fe, #ddd6fe); color: var(--clay-accent); }
.clay-chip-pink   { background: linear-gradient(135deg, #fce7f3, #fbcfe8); color: var(--clay-accent-alt); }
.clay-chip-sky    { background: linear-gradient(135deg, #e0f2fe, #bae6fd); color: #0369a1; }
.clay-chip-green  { background: linear-gradient(135deg, #d1fae5, #a7f3d0); color: #047857; }
.clay-chip-amber  { background: linear-gradient(135deg, #fef3c7, #fde68a); color: #b45309; }
.clay-chip-icon { font-size: 1rem; }

.clay-badge {
  display: inline-block;
  padding: 0.35rem 0.9rem;
  border-radius: 9999px;
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  background: linear-gradient(135deg, var(--clay-accent-light), var(--clay-accent));
  color: #fff;
  box-shadow: 0 6px 14px rgba(139, 92, 246, 0.30);
}
.clay-badge-pink { background: linear-gradient(135deg, #f472b6, var(--clay-accent-alt)); box-shadow: 0 6px 14px rgba(219,39,119,.3); }
.clay-badge-sky  { background: linear-gradient(135deg, #38bdf8, var(--clay-info)); box-shadow: 0 6px 14px rgba(14,165,233,.3); }

/* ==========================================================
   11. CARDS: FORM / CONTAINER / EXPANDER / TABS
   ========================================================== */
[data-testid="stForm"] {
  background: rgba(255, 255, 255, 0.75);
  border: none !important;
  border-radius: var(--r-xl) !important;
  box-shadow: var(--clay-card);
  padding: 1.8rem 1.8rem 1.2rem 1.8rem !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255, 255, 255, 0.72) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: none !important;
  border-radius: var(--r-lg) !important;
  box-shadow: var(--clay-card);
  padding: 1.3rem 1.5rem 1.5rem 1.5rem !important;
  transition: transform .4s ease, box-shadow .4s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: var(--clay-card-lift); }
[data-testid="stVerticalBlockBorder"] { border: none !important; border-radius: var(--r-lg) !important; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] h3 { margin-top: 0.2rem; }

/* Expander: card when closed, recessed when open */
[data-testid="stExpander"] details {
  background: rgba(255, 255, 255, 0.78) !important;
  border: none !important;
  border-radius: var(--r-lg) !important;
  box-shadow: var(--clay-card);
  overflow: hidden;
}
[data-testid="stExpander"] summary {
  border-radius: var(--r-lg) !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-foreground) !important;
  padding: 1rem 1.3rem !important;
}
[data-testid="stExpander"] summary:hover { background: rgba(124, 58, 237, 0.07) !important; }
[data-testid="stExpander"] details[open] { box-shadow: var(--clay-pressed); }
[data-testid="stExpander"] details[open] summary { border-bottom: 1px solid rgba(124, 58, 237, 0.14); }

/* Tabs */
[data-testid="stTabs"] [role="tablist"] { gap: 0.5rem; }
[data-testid="stTabs"] [role="tab"] {
  background: rgba(255, 255, 255, 0.7) !important;
  border: none !important;
  border-radius: 9999px !important;
  padding: 0.7rem 1.4rem !important;
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-muted) !important;
  box-shadow: var(--clay-card);
  transition: all .25s ease;
}
[data-testid="stTabs"] [role="tab"]:hover { transform: translateY(-3px); color: var(--clay-accent) !important; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: linear-gradient(135deg, var(--clay-accent-light), var(--clay-accent)) !important;
  color: #ffffff !important;
  box-shadow: var(--clay-btn);
}

/* Radio & checkbox -> soft clay pills */
[data-testid="stRadio"] > div { gap: 0.6rem; }
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
  border-radius: var(--r-sm) !important;
  padding: 0.7rem 1.1rem !important;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: var(--clay-card);
  transition: transform .25s ease, box-shadow .25s ease, background .25s ease;
  min-height: 44px;
}
[data-testid="stRadio"] label:hover,
[data-testid="stCheckbox"] label:hover { transform: translateY(-3px); background: #ffffff; }
[data-testid="stRadio"] label:has(input:checked),
[data-testid="stCheckbox"] label:has(input:checked) {
  background: linear-gradient(135deg, rgba(167,139,250,0.30), rgba(124,58,237,0.20)) !important;
  box-shadow: var(--clay-pressed);
}
[data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stRadio"] label:has(input:checked) span,
[data-testid="stCheckbox"] label:has(input:checked) p {
  color: var(--clay-accent) !important;
  font-weight: 800 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  background: rgba(255, 255, 255, 0.85);
}

/* ==========================================================
   12. DATA & CHARTS
   ========================================================== */
[data-testid="stDataFrame"],
[data-testid="stPlotlyChart"] {
  border-radius: var(--r-lg) !important;
  box-shadow: var(--clay-card);
  overflow: hidden;
  background: rgba(255, 255, 255, 0.75);
  transition: transform .4s ease, box-shadow .4s ease;
}
[data-testid="stDataFrame"]:hover,
[data-testid="stPlotlyChart"]:hover { box-shadow: var(--clay-card-lift); }

[data-testid="stPlotlyChart"] { padding: 0.6rem; }

/* ==========================================================
   13. MISC
   ========================================================== */
hr, [data-testid="stDivider"] {
  border: 0 !important;
  height: 2px !important;
  background: linear-gradient(90deg, rgba(124,58,237,0.35), rgba(219,39,119,0.22), rgba(14,165,233,0.15), transparent) !important;
  margin: 1.6rem 0 !important;
}

/* Tooltip */
[data-testid="stTooltip"] {
  background: var(--clay-foreground) !important;
  border-radius: var(--r-sm) !important;
  box-shadow: var(--clay-card);
  font-family: 'DM Sans', sans-serif;
}

/* Progress bar */
[data-testid="stProgress"] > div > div > div > div {
  background: linear-gradient(90deg, var(--clay-accent-light), var(--clay-accent), var(--clay-accent-alt)) !important;
  border-radius: 9999px !important;
}

/* Status / success blocks in sidebar */
[data-testid="stSidebar"] [data-testid="stAlert"] {
  background: rgba(255, 255, 255, 0.9) !important;
  box-shadow: var(--clay-card), inset 5px 0 0 var(--clay-success) !important;
}

/* Chat / status labels */
[data-testid="stWidgetLabel"] p, label[data-testid="stWidgetLabel"] {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  color: var(--clay-foreground) !important;
}

/* Balloons / toast stay themed */
[data-testid="stToast"] { border-radius: var(--r-sm) !important; box-shadow: var(--clay-card-lift) !important; }

/* ==========================================================
   14. HERO (used by ui_components.setup_page)
   ========================================================== */
.clay-hero {
  position: relative;
  overflow: hidden;
  border-radius: var(--r-xl);
  padding: 2.6rem 2.4rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.90), rgba(255,255,255,0.66));
  backdrop-filter: blur(26px);
  -webkit-backdrop-filter: blur(26px);
  box-shadow: var(--clay-card);
  margin-bottom: 1.4rem;
}
.clay-hero::after {
  content: "";
  position: absolute;
  top: -60px; right: -60px;
  width: 240px; height: 240px;
  border-radius: 9999px;
  background: radial-gradient(circle at 30% 30%, rgba(167,139,250,0.55), rgba(124,58,237,0.05));
  filter: blur(6px);
  pointer-events: none;
}
.clay-hero-row { display: flex; align-items: center; gap: 1.4rem; position: relative; z-index: 1; }
.clay-hero-logo {
  width: 92px; height: 92px;
  border-radius: 9999px;
  object-fit: cover;
  box-shadow: var(--clay-btn);
  animation: clay-breathe 6s ease-in-out infinite;
  flex-shrink: 0;
  background: #fff;
}
.clay-hero h1 {
  font-family: 'Nunito', sans-serif !important;
  font-weight: 900 !important;
  font-size: clamp(2.1rem, 4.6vw, 3.5rem) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.03em !important;
  margin: 0 !important;
  background: linear-gradient(120deg, var(--clay-foreground) 20%, var(--clay-accent) 62%, var(--clay-accent-alt) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
.clay-hero-sub {
  color: var(--clay-muted) !important;
  font-size: 1.06rem !important;
  font-weight: 500 !important;
  margin: 0.55rem 0 0 0 !important;
  max-width: 62ch;
}
.clay-hero-badges { display: flex; flex-wrap: wrap; gap: 0.7rem; margin-top: 1.25rem; position: relative; z-index: 1; }

/* Stat orbs */
.clay-orbs {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.1rem;
  margin: 1.4rem 0 0.4rem 0;
}
.clay-orb {
  position: relative;
  overflow: hidden;
  text-align: center;
  padding: 1.35rem 1rem;
  border-radius: var(--r-lg);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(18px);
  box-shadow: var(--clay-card);
  transition: transform .4s ease, box-shadow .4s ease;
  animation: clay-breathe 6s ease-in-out infinite;
}
.clay-orb:nth-child(2) { animation-delay: 1.5s; }
.clay-orb:nth-child(3) { animation-delay: 3s; }
.clay-orb:nth-child(4) { animation-delay: 4.5s; }
.clay-orb:hover { transform: translateY(-8px); box-shadow: var(--clay-card-lift); }
.clay-orb-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 56px; height: 56px;
  border-radius: 9999px;
  font-size: 1.5rem;
  margin-bottom: 0.7rem;
  box-shadow: var(--clay-btn);
}
.clay-orb-icon.violet { background: linear-gradient(135deg, #a78bfa, #7c3aed); }
.clay-orb-icon.pink   { background: linear-gradient(135deg, #f472b6, #db2777); }
.clay-orb-icon.sky    { background: linear-gradient(135deg, #38bdf8, #0ea5e9); }
.clay-orb-icon.green  { background: linear-gradient(135deg, #34d399, #10b981); }
.clay-orb-value {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 1.65rem;
  line-height: 1.1;
  color: var(--clay-foreground);
  display: block;
}
.clay-orb-label {
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 0.74rem;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--clay-muted);
  display: block;
  margin-top: 0.3rem;
}

@media (max-width: 900px) {
  .clay-orbs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .clay-hero { padding: 1.8rem 1.4rem; }
  .clay-hero-row { flex-direction: column; align-items: flex-start; }
  section.main .block-container, [data-testid="stMainBlockContainer"] { border-radius: var(--r-lg); padding-left: 0.6rem; padding-right: 0.6rem; }
}

/* ==========================================================
   15. ANIMATIONS
   ========================================================== */
@keyframes clay-float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-20px) rotate(2deg); }
}
@keyframes clay-float-delayed {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-15px) rotate(-2deg); }
}
@keyframes clay-float-slow {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-30px) rotate(5deg); }
}
@keyframes clay-breathe {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.02); }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
}
</style>
"""
