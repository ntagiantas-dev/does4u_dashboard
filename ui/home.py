"""Home / Welcome page — δείχνεται όταν δεν έχει επιλεγεί plugin.

Public API:
- render_home(registry) → None
"""

from typing import Optional

import streamlit as st

from config.i18n import t
from core.plugin_registry import PluginRegistry
from core import config_manager as cm


HOME_CSS = """
<style>
.d4u-home-hero {
    text-align: center;
    padding: 3rem 1rem 2rem 1rem;
}
.d4u-home-logo {
    font-size: 4rem;
    line-height: 1;
    margin-bottom: 1rem;
}
.d4u-home-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    margin: 0 0 0.5rem 0;
}
.d4u-home-subtitle {
    font-size: 1rem;
    color: var(--text-muted);
    margin: 0;
}

.d4u-home-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.d4u-home-card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 0.5rem 0;
}
.d4u-home-card-body {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin: 0;
    line-height: 1.5;
}

.d4u-home-alert {
    padding: 1rem 1.25rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
    background: rgba(245, 158, 11, 0.08);
    border-left: 4px solid var(--warning);
    margin-bottom: 1rem;
}
.d4u-home-alert-title {
    font-weight: 600;
    color: var(--text);
    margin: 0 0 0.25rem 0;
}
.d4u-home-alert-body {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin: 0;
}

.d4u-home-hint {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 2rem;
    font-style: italic;
}
</style>
"""


def _count_tools(registry: PluginRegistry) -> int:
    total = 0
    for plugin in registry.all():
        total += len(plugin.list_tools())
    return total


def _render_hero() -> None:
    st.markdown(
        '<div class="d4u-home-hero">'
        '<div class="d4u-home-logo">🎯</div>'
        f'<div class="d4u-home-title">{t("home.title")}</div>'
        f'<div class="d4u-home-subtitle">{t("home.subtitle")}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_stats(registry: PluginRegistry) -> None:
    if registry.count() == 0:
        return

    has_key = bool(cm.get_api_key(cm.get_active_provider()))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("home.stats_plugins"), registry.count())
    with col2:
        st.metric(t("home.stats_tools"), _count_tools(registry))
    with col3:
        if has_key:
            st.metric(t("home.stats_status"), t("home.stats_ready"))
        else:
            st.metric(t("home.stats_status"), t("home.stats_no_key"))


def _render_missing_key_alert() -> None:
    """Δείχνει alert αν λείπει API key και υπάρχουν plugins."""
    if cm.get_api_key(cm.get_active_provider()):
        return
    st.markdown(
        f'<div class="d4u-home-alert">'
        f'  <div class="d4u-home-alert-title">{t("home.missing_key_title")}</div>'
        f'  <div class="d4u-home-alert-body">{t("home.missing_key_body")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_no_plugins() -> None:
    st.markdown(
        f'<div class="d4u-home-card">'
        f'  <div class="d4u-home-card-title">{t("home.no_plugins_title")}</div>'
        f'  <div class="d4u-home-card-body">{t("home.no_plugins_body")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_tip() -> None:
    st.markdown(
        f'<div class="d4u-home-card">'
        f'  <div class="d4u-home-card-title">{t("home.tip_title")}</div>'
        f'  <div class="d4u-home-card-body">{t("home.tip_body")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_home(registry: Optional[PluginRegistry]) -> None:
    """Render τη welcome page.

    Args:
        registry: PluginRegistry (μπορεί να είναι None).
    """
    st.markdown(HOME_CSS, unsafe_allow_html=True)
    _render_hero()

    if registry is None or registry.count() == 0:
        _render_no_plugins()
        _render_tip()
        return

    _render_missing_key_alert()
    _render_stats(registry)

    st.markdown(
        f'<div class="d4u-home-hint">{t("home.subtitle")}</div>',
        unsafe_allow_html=True,
    )