import streamlit as st
from config.theme import apply_theme, DEFAULT_THEME
from config.i18n import t, get_lang, set_lang, all_langs, lang_label

st.set_page_config(
    page_title="does4u Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = DEFAULT_THEME

apply_theme(st.session_state.theme_mode)

with st.sidebar:
    st.markdown(f"## {t('sidebar.brand')}")
    st.caption(t("app.tagline"))

    st.markdown("---")

    is_dark = st.session_state.theme_mode == "dark"
    new_val = st.toggle(t("sidebar.theme_dark"), value=is_dark, key="dark_toggle")
    if new_val != is_dark:
        st.session_state.theme_mode = "dark" if new_val else "light"
        st.rerun()

    st.markdown("---")

    langs = all_langs()
    current_lang = get_lang()
    current_index = langs.index(current_lang) if current_lang in langs else 0
    chosen = st.radio(
        t("sidebar.language"),
        options=langs,
        index=current_index,
        format_func=lang_label,
        key="lang_radio",
    )
    if chosen != current_lang:
        set_lang(chosen)
        st.rerun()

    st.markdown("---")
    st.caption(t("app.phase"))

st.markdown(f'<div class="d4u-title">{t("welcome.title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="d4u-subtitle">{t("welcome.subtitle")}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(t("metric.progress"), "5/45", t("metric.progress_delta"))
with col2:
    st.metric(t("metric.plugins"), "0", t("metric.plugins_delta"))
with col3:
    st.metric(t("metric.theme"), "Dark/Light", t("metric.theme_delta"))

st.markdown("---")

col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
with col1:
    st.button(t("button.primary"), use_container_width=True)
with col2:
    st.button(t("button.accent"), type="primary", use_container_width=True)
with col3:
    st.button(t("button.cancel"), use_container_width=True)

st.markdown("---")

st.markdown(
    f'<div class="d4u-card">'
    f'<h3 style="margin-top: 0;">{t("card.title")}</h3>'
    f'<p>{t("card.body")}</p>'
    f'</div>',
    unsafe_allow_html=True,
)

st.write("")

st.success(t("alert.success"))
st.warning(t("alert.warning"))
st.error(t("alert.error"))

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.text_input(t("input.name"), placeholder=t("input.name_placeholder"))
    st.number_input(t("input.amount"), min_value=0.0, value=100.0)
with col2:
    st.text_area(t("input.notes"), placeholder=t("input.notes_placeholder"))
    st.selectbox(
        t("input.select"),
        [t("input.select_option") + " 1", t("input.select_option") + " 2", t("input.select_option") + " 3"],
    )

st.markdown("---")
st.caption(f"🎨 {t('app.title')} • {t('app.phase')}")