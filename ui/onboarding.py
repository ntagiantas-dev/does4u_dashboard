"""Onboarding — πρώτη εκκίνηση.

Δείχνεται μόνο την πρώτη φορά που ανοίγει ο χρήστης το dashboard.
Αποθηκεύει provider + API key + γλώσσα + theme στο config.

Public API:
- is_onboarding_needed() → bool
- render_onboarding() → None
"""

import streamlit as st

from config.i18n import t, get_lang, set_lang, all_langs, lang_label
from config.theme import apply_theme, DEFAULT_THEME
from core import config_manager as cm


PROVIDER_LABELS = {
    "openai": "OpenAI (GPT)",
    "anthropic": "Anthropic (Claude)",
    "xai": "xAI (Grok)",
}


ONBOARDING_CSS = """
<style>
.d4u-ob-wrapper {
    max-width: 640px;
    margin: 2rem auto;
    padding: 0 1rem;
}
.d4u-ob-hero {
    text-align: center;
    margin-bottom: 2rem;
}
.d4u-ob-logo {
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.d4u-ob-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}
.d4u-ob-subtitle {
    font-size: 1rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
}
.d4u-ob-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.d4u-ob-step {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.25rem;
}
.d4u-ob-hint {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
}
.d4u-ob-warning {
    background: rgba(245, 158, 11, 0.1);
    border-left: 3px solid var(--warning);
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 0.8rem;
    color: var(--text);
    margin-top: 0.5rem;
}
.d4u-ob-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 2rem;
}
</style>
"""


# ---------- State ----------

def _init_state() -> None:
    if "ob_provider" not in st.session_state:
        st.session_state.ob_provider = cm.get_active_provider() or "openai"
    if "ob_lang" not in st.session_state:
        st.session_state.ob_lang = get_lang()
    if "ob_theme" not in st.session_state:
        st.session_state.ob_theme = cm.get_theme() or DEFAULT_THEME


# ---------- Public API ----------

def is_onboarding_needed() -> bool:
    """Επιστρέφει True αν ο χρήστης ΔΕΝ έχει περάσει το onboarding."""
    return not cm.is_onboarding_completed()


def _save_and_finish(provider: str, api_key: str, lang: str, theme: str) -> None:
    """Αποθηκεύει όλα στο config και μαρκάρει το onboarding ολοκληρωμένο."""
    if api_key.strip():
        cm.set_api_key(provider, api_key.strip())
    cm.set_active_provider(provider)
    cm.set_language(lang)
    cm.set_theme(theme)
    set_lang(lang)
    cm.mark_onboarding_completed()


# ---------- Rendering ----------

def _render_hero() -> None:
    st.markdown(
        '<div class="d4u-ob-hero">'
        '<div class="d4u-ob-logo">🎯</div>'
        f'<div class="d4u-ob-title">{t("onboarding.welcome")}</div>'
        f'<div class="d4u-ob-subtitle">{t("onboarding.subtitle")}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_provider_step() -> str:
    st.markdown('<div class="d4u-ob-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="d4u-ob-step">{t("onboarding.step_provider")}</div>'
        f'<div class="d4u-ob-hint">{t("onboarding.step_provider_hint")}</div>',
        unsafe_allow_html=True,
    )

    providers = list(PROVIDER_LABELS.keys())
    current = st.session_state.ob_provider
    try:
        idx = providers.index(current)
    except ValueError:
        idx = 0

    chosen = st.selectbox(
        t("onboarding.provider_label"),
        options=providers,
        index=idx,
        format_func=lambda p: PROVIDER_LABELS.get(p, p),
        key="ob_provider_select",
    )
    st.session_state.ob_provider = chosen
    st.markdown('</div>', unsafe_allow_html=True)
    return chosen


def _render_key_step(provider: str) -> str:
    st.markdown('<div class="d4u-ob-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="d4u-ob-step">{t("onboarding.step_key")}</div>'
        f'<div class="d4u-ob-hint">{t("onboarding.step_key_hint")}</div>',
        unsafe_allow_html=True,
    )

    existing = cm.get_api_key(provider)
    key = st.text_input(
        t("onboarding.key_label"),
        value=existing,
        type="password",
        placeholder=t("onboarding.key_placeholder"),
        key=f"ob_key_{provider}",
    )

    st.markdown(
        f'<div class="d4u-ob-warning">{t("onboarding.privacy_warning")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return key


def _render_prefs_step() -> tuple:
    st.markdown('<div class="d4u-ob-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="d4u-ob-step">{t("onboarding.step_prefs")}</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        langs = all_langs()
        current_lang = st.session_state.ob_lang
        try:
            lang_idx = langs.index(current_lang)
        except ValueError:
            lang_idx = 0
        chosen_lang = st.radio(
            t("onboarding.lang_label"),
            options=langs,
            index=lang_idx,
            format_func=lang_label,
            key="ob_lang_radio",
        )
        st.session_state.ob_lang = chosen_lang

    with col2:
        themes = ["dark", "light"]
        theme_labels = {
            "dark": t("onboarding.theme_dark"),
            "light": t("onboarding.theme_light"),
        }
        current_theme = st.session_state.ob_theme
        try:
            theme_idx = themes.index(current_theme)
        except ValueError:
            theme_idx = 0
        chosen_theme = st.radio(
            t("onboarding.theme_label"),
            options=themes,
            index=theme_idx,
            format_func=lambda x: theme_labels.get(x, x),
            key="ob_theme_radio",
        )
        st.session_state.ob_theme = chosen_theme

    st.markdown('</div>', unsafe_allow_html=True)
    return chosen_lang, chosen_theme


def _render_actions(provider: str, api_key: str, lang: str, theme: str) -> None:
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            t("onboarding.finish"),
            type="primary",
            use_container_width=True,
            key="ob_finish",
        ):
            if not api_key.strip():
                st.warning(t("onboarding.key_required"))
            else:
                _save_and_finish(provider, api_key, lang, theme)
                st.rerun()

    with col2:
        if st.button(
            t("onboarding.skip"),
            use_container_width=True,
            key="ob_skip",
        ):
            _save_and_finish(provider, "", lang, theme)
            st.rerun()

    st.caption(t("onboarding.skip_hint"))


# ---------- Public entry ----------

def render_onboarding() -> None:
    """Render της σελίδας onboarding.

    Καλείται από το app.py όταν is_onboarding_needed() is True.
    """
    _init_state()
    apply_theme(st.session_state.ob_theme)
    st.markdown(ONBOARDING_CSS, unsafe_allow_html=True)

    st.markdown('<div class="d4u-ob-wrapper">', unsafe_allow_html=True)
    _render_hero()

    provider = _render_provider_step()
    api_key = _render_key_step(provider)
    lang, theme = _render_prefs_step()

    # Apply theme live (να βλέπει ο χρήστης τι διαλέγει)
    if theme != st.session_state.get("_ob_last_theme"):
        st.session_state["_ob_last_theme"] = theme
        st.rerun()

    _render_actions(provider, api_key, lang, theme)

    st.markdown(
        f'<div class="d4u-ob-footer">{t("onboarding.footer")}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)