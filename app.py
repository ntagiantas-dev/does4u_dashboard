import streamlit as st
from config.theme import apply_theme, DEFAULT_THEME

st.set_page_config(
    page_title="does4u Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = DEFAULT_THEME
if "theme_toggle" not in st.session_state:
    st.session_state.theme_toggle = (st.session_state.theme_mode == "dark")


def _on_toggle_change():
    st.session_state.theme_mode = "dark" if st.session_state.theme_toggle else "light"


apply_theme(st.session_state.theme_mode)

with st.sidebar:
    st.markdown("## 🎯 does4u")
    st.caption("Data • AI • Automation")

    st.markdown("---")

    st.toggle("🌙 Dark mode", key="theme_toggle", on_change=_on_toggle_change)

    st.markdown("---")
    st.caption("Phase 1.1 • Theme System")

st.markdown('<div class="d4u-title">Καλώς ήρθες, Μήτσο 👋</div>', unsafe_allow_html=True)
st.markdown('<div class="d4u-subtitle">Δείγμα του theme • Phase 1.1</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Πρόοδος", "4/42", "+1 σήμερα")
with col2:
    st.metric("Plugins", "0", "σε ανάπτυξη")
with col3:
    st.metric("Theme", "Dark/Light", "✓")

st.markdown("---")

col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    st.button("Primary", use_container_width=True)
with col2:
    st.button("Accent", type="primary", use_container_width=True)
with col3:
    st.button("Άκυρο", use_container_width=True)

st.markdown("---")

st.markdown(
    '<div class="d4u-card">'
    '<h3 style="margin-top: 0;">🎨 Premium Card</h3>'
    '<p>Έτσι θα φαίνονται τα cards — με απαλές σκιές, '
    'στρογγυλεμένες γωνίες και consistent spacing.</p>'
    '</div>',
    unsafe_allow_html=True,
)

st.write("")

st.success("✅ Επιτυχία — αυτό είναι ένα success message")
st.warning("⚠️ Προσοχή — αυτό είναι ένα warning")
st.error("❌ Σφάλμα — αυτό είναι ένα error")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.text_input("Όνομα", placeholder="π.χ. Μήτσος")
    st.number_input("Ποσό (€)", min_value=0.0, value=100.0)
with col2:
    st.text_area("Σημειώσεις", placeholder="Γράψε κάτι...")
    st.selectbox("Επιλογή", ["Επιλογή 1", "Επιλογή 2", "Επιλογή 3"])

st.markdown("---")
st.caption("🎨 does4u Dashboard • Phase 1.1 — Theme System")
