import streamlit as st


THEMES = {
    "light": {
        "primary":       "#1F4E79",
        "primary_hover": "#2C6398",
        "accent":        "#FFC000",
        "accent_hover":  "#E6A800",
        "bg":            "#F5F7FA",
        "surface":       "#FFFFFF",
        "surface_2":     "#EFF3F8",
        "text":          "#0F172A",
        "text_muted":    "#64748B",
        "border":        "#E2E8F0",
        "success":       "#10B981",
        "warning":       "#F59E0B",
        "error":         "#EF4444",
        "sidebar_bg":    "#1F4E79",
        "sidebar_text":  "#F0F4F8",
        "sidebar_muted": "#A8C0DC",
    },
    "dark": {
        "primary":       "#4A90D9",
        "primary_hover": "#5FA3E8",
        "accent":        "#FFC000",
        "accent_hover":  "#E6A800",
        "bg":            "#0B1622",
        "surface":       "#162234",
        "surface_2":     "#1E2D42",
        "text":          "#F0F4F8",
        "text_muted":    "#94A3B8",
        "border":        "#2A3F5A",
        "success":       "#34D399",
        "warning":       "#FBBF24",
        "error":         "#F87171",
        "sidebar_bg":    "#0A1422",
        "sidebar_text":  "#F0F4F8",
        "sidebar_muted": "#7A8FA8",
    },
}

DEFAULT_THEME = "dark"


def get_theme(mode):
    return THEMES.get(mode, THEMES[DEFAULT_THEME])


def build_css(mode):
    c = get_theme(mode)

    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary:        __PRIMARY__;
        --primary-hover:  __PRIMARY_HOVER__;
        --accent:         __ACCENT__;
        --accent-hover:   __ACCENT_HOVER__;
        --bg:             __BG__;
        --surface:        __SURFACE__;
        --surface-2:      __SURFACE_2__;
        --text:           __TEXT__;
        --text-muted:     __TEXT_MUTED__;
        --border:         __BORDER__;
        --success:        __SUCCESS__;
        --warning:        __WARNING__;
        --error:          __ERROR__;
        --sidebar-bg:     __SIDEBAR_BG__;
        --sidebar-text:   __SIDEBAR_TEXT__;
        --sidebar-muted:  __SIDEBAR_MUTED__;
        --radius-sm:      6px;
        --radius:         10px;
        --radius-lg:      14px;
    }

    /* ========== FONTS & BASE ========== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ========== BACKGROUND - MAIN AREA ONLY ========== */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    section.main,
    .main,
    .main .block-container,
    .main div[data-testid="stVerticalBlock"],
    .main div[data-testid="stHorizontalBlock"] {
        background-color: __BG__ !important;
        color: __TEXT__ !important;
    }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer {
        visibility: hidden;
    }

    /* ========== SIDEBAR - ΠΑΝΤΑ ΣΚΟΥΡΟ ΜΠΛΕ ========== */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div > div,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: __SIDEBAR_BG__ !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: __SIDEBAR_TEXT__ !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: __SIDEBAR_MUTED__ !important;
    }

    /* ========== TOGGLE (sidebar) ========== */
    [data-testid="stSidebar"] [data-baseweb="checkbox"] div[role="checkbox"] {
        background-color: rgba(255,255,255,0.15) !important;
    }

    [data-testid="stSidebar"] [data-baseweb="checkbox"] div[role="checkbox"][aria-checked="true"] {
        background-color: __ACCENT__ !important;
    }

    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {
        color: __TEXT__ !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    p, span, label, div {
        color: __TEXT__;
    }

    /* ========== BUTTONS - ΟΛΑ ΤΑ STATES ========== */
    .stButton > button,
    .stButton > button:focus,
    .stButton > button:focus-visible,
    .stButton > button:active,
    .stButton > button:visited,
    .stButton > button:hover,
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-secondary"]:hover,
    button[data-testid="baseButton-secondary"]:focus,
    button[data-testid="baseButton-secondary"]:active,
    button[kind="secondary"],
    button[kind="secondary"]:hover,
    button[kind="secondary"]:focus,
    button[kind="secondary"]:active {
        background: var(--primary) !important;
        background-color: var(--primary) !important;
        background-image: none !important;
        color: #FFFFFF !important;
        border: 1px solid var(--primary) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08) !important;
        text-shadow: none !important;
    }

    .stButton > button:hover,
    button[data-testid="baseButton-secondary"]:hover,
    button[kind="secondary"]:hover {
        background: var(--primary-hover) !important;
        background-color: var(--primary-hover) !important;
        background-image: none !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.12) !important;
    }

    /* Primary type button (Accent κίτρινο) */
    .stButton > button[kind="primary"],
    .stButton > button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:focus,
    .stButton > button[kind="primary"]:focus-visible,
    .stButton > button[kind="primary"]:active,
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-primary"]:focus,
    button[data-testid="baseButton-primary"]:active {
        background: var(--accent) !important;
        background-color: var(--accent) !important;
        background-image: none !important;
        color: #1F2937 !important;
        border: 1px solid var(--accent) !important;
    }

    .stButton > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: var(--accent-hover) !important;
        background-color: var(--accent-hover) !important;
        background-image: none !important;
        color: #1F2937 !important;
    }

    /* Κείμενο μέσα στο button - να μην αλλάζει χρώμα */
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    button[data-testid="baseButton-secondary"] p,
    button[data-testid="baseButton-secondary"] span {
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"] p,
    .stButton > button[kind="primary"] span,
    button[data-testid="baseButton-primary"] p,
    button[data-testid="baseButton-primary"] span {
        color: #1F2937 !important;
    }

    .stButton > button:disabled {
        background: var(--primary) !important;
        background-color: var(--primary) !important;
        background-image: none !important;
        color: #FFFFFF !important;
        opacity: 0.5 !important;
        cursor: not-allowed !important;
    }

    /* ========== INPUTS ========== */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: __SURFACE__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: var(--radius-sm) !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {
        border-color: __PRIMARY__ !important;
        box-shadow: 0 0 0 2px rgba(31,78,121,0.15) !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background-color: __SURFACE__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: var(--radius-sm) !important;
        color: __TEXT__ !important;
    }

    /* ========== METRICS ========== */
    [data-testid="stMetric"] {
        background-color: __SURFACE__ !important;
        padding: 1.25rem !important;
        border-radius: var(--radius) !important;
        border: 1px solid __BORDER__ !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }

    [data-testid="stMetric"] * {
        color: __TEXT__ !important;
    }

    [data-testid="stMetricValue"] {
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: __TEXT_MUTED__ !important;
        font-weight: 500 !important;
    }

    /* ========== ALERTS ========== */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        border: 1px solid __BORDER__ !important;
    }

    /* ========== CUSTOM CLASSES ========== */
    .d4u-card {
        background-color: __SURFACE__;
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid __BORDER__;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.15s ease;
    }

    .d4u-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .d4u-title {
        font-size: 2rem;
        font-weight: 700;
        color: __TEXT__;
        margin-bottom: 0.25rem;
    }

    .d4u-subtitle {
        font-size: 1rem;
        color: __TEXT_MUTED__;
        margin-bottom: 2rem;
    }

    .d4u-accent {
        color: __ACCENT__;
    }

    /* ========== MISC ========== */
    hr {
        border-color: __BORDER__ !important;
        margin: 2rem 0 !important;
    }

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: __BG__;
    }
    ::-webkit-scrollbar-thumb {
        background: __BORDER__;
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: __TEXT_MUTED__;
    }
    </style>
    """.replace("__SURFACE_2__",     c["surface_2"]) \
       .replace("__SURFACE__",       c["surface"]) \
       .replace("__TEXT_MUTED__",    c["text_muted"]) \
       .replace("__TEXT__",          c["text"]) \
       .replace("__PRIMARY_HOVER__", c["primary_hover"]) \
       .replace("__PRIMARY__",       c["primary"]) \
       .replace("__ACCENT_HOVER__",  c["accent_hover"]) \
       .replace("__ACCENT__",        c["accent"]) \
       .replace("__BG__",            c["bg"]) \
       .replace("__BORDER__",        c["border"]) \
       .replace("__SUCCESS__",       c["success"]) \
       .replace("__WARNING__",       c["warning"]) \
       .replace("__ERROR__",         c["error"]) \
       .replace("__SIDEBAR_BG__",    c["sidebar_bg"]) \
       .replace("__SIDEBAR_TEXT__",  c["sidebar_text"]) \
       .replace("__SIDEBAR_MUTED__", c["sidebar_muted"])


def apply_theme(mode):
    st.markdown(build_css(mode), unsafe_allow_html=True)
