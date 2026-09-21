import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(
    page_title="does4u Dashboard",
    page_icon="🎯",
    layout="wide",
)

# Χρώματα does4u
PRIMARY = "#1F4E79"
ACCENT = "#FFC000"

# Custom CSS για να φαίνονται τα χρώματα
st.markdown(f"""
<style>
    .main-title {{
        color: {PRIMARY};
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-top: 3rem;
    }}
    .subtitle {{
        color: {ACCENT};
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 3rem;
    }}
    .info-box {{
        background-color: {PRIMARY};
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }}
</style>
""", unsafe_allow_html=True)

# Κύριο περιεχόμενο
st.markdown('<div class="main-title">Hello does4u</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Data • AI • Automation</div>', unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"""
<div class="info-box">
    <strong>✅ Smoke Test OK</strong><br>
    Streamlit δουλεύει • Venv δουλεύει • Browser δουλεύει
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# Sidebar με πληροφορίες
with st.sidebar:
    st.title("🎯 does4u Dashboard")
    st.caption("Smoke Test v0.1")
    st.markdown("---")
    st.write("**Κατάσταση:**")
    st.write("✅ Python 3.13")
    st.write("✅ Streamlit")
    st.write("✅ Venv ενεργό")
    st.write("✅ Όλα τα πακέτα")
    st.markdown("---")
    st.caption("Phase 0 — Setup")