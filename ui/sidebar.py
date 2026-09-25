"""Sidebar component — VS Code-style navigation.

Διαβάζει τα plugins από τον registry, τα ομαδοποιεί ανά category,
και επιτρέπει navigation. ΔΕΝ ξέρει συγκεκριμένα plugins — όλα
γίνονται dynamically.

Public API:
- render_sidebar(registry) → None
- get_active_plugin() → Optional[str]
- set_active_plugin(name) → None
"""

from typing import Dict, List, Optional

import streamlit as st

from config.i18n import t, get_lang, set_lang, all_langs, lang_label
from config.theme import apply_theme, DEFAULT_THEME
from core.plugin_registry import PluginRegistry
from core import config_manager as cm


SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] .d4u-sidebar-header {
    padding: 0.5rem 0 1rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    margin-bottom: 1rem;
}
[data-testid="stSidebar"] .d4u-logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--sidebar-text);
    margin: 0;
    letter-spacing: -0.02em;
}
[data-testid="stSidebar"] .d4u-tagline {
    font-size: 0.75rem;
    color: var(--sidebar-muted);
    margin: 0.2rem 0 0 0;
}

[data-testid="stSidebar"] .d4u-category {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--sidebar-muted);
    margin: 1rem 0 0.4rem 0;
    padding-left: 0.25rem;
}

[data-testid="stSidebar"] .d4u-plugin-btn {
    display: block;
    width: 100%;
    text-align: left;
    padding: 0.4rem 0.75rem;
    margin: 0.15rem 0;
    border-radius: 6px;
    font-size: 0.9rem;
    color: var(--sidebar-text);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: background 0.12s ease;
}
[data-testid="stSidebar"] .d4u-plugin-btn:hover {
    background: rgba(255, 255, 255, 0.08);
}
[data-testid="stSidebar"] .d4u-plugin-btn.active {
    background: rgba(255, 192, 0, 0.18);
    color: var(--accent);
    font-weight: 600;
}

[data-testid="stSidebar"] .d4u-sidebar-footer {
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 0.75rem;
    color: var(--sidebar-muted);
}

[data-testid="stSidebar"] .d4u-empty {
    padding: 1rem 0.5rem;
    text-align: center;
    font-size: 0.85rem;
    color: var(--sidebar-muted);
    font-style: italic;
}

/* Streamlit buttons μέσα στο sidebar - reset για να φαίνονται σαν menu items */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    background-image: none !important;
    color: var(--sidebar-text) !important;
    border: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.4rem 0.75rem !important;
    font-weight: 400 !important;
    box-shadow: none !important;
    transform: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: var(--sidebar-text) !important;
    transform: none !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button p {
    color: var(--sidebar-text) !important;
    font-size: 0.9rem !important;
}
</style>
"""


# ---------- Session state ----------

def _init_state() -> None:
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = cm.get_theme() or DEFAULT_THEME
    if "lang" not in st.session_state:
        st.session_state.lang = cm.get_language() or get_lang()
    if "active_plugin" not in st.session_state:
        st.session_state.active_plugin = None


def get_active_plugin() -> Optional[str]:
    """Επιστρέφει το όνομα του ενεργού plugin (ή None)."""
    return st.session_state.get("active_plugin")


def set_active_plugin(name: Optional[str]) -> None:
    """Ορίζει το ενεργό plugin. ΔΕΝ κάνει rerun (το κάνει ο caller)."""
    st.session_state.active_plugin = name


# ---------- Rendering ----------

def _render_header() -> None:
    st.markdown(
        '<div class="d4u-sidebar-header">'
        '<div class="d4u-logo">🎯 does4u</div>'
        '<div class="d4u-tagline">Data • AI • Automation</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_controls() -> None:
    """Theme toggle + language selector."""

    # Theme toggle
    is_dark = st.session_state.theme_mode == "dark"
    new_val = st.toggle(
        t("sidebar.theme_dark"),
        value=is_dark,
        key="theme_toggle_sidebar",
    )
    if new_val != is_dark:
        new_mode = "dark" if new_val else "light"
        st.session_state.theme_mode = new_mode
        cm.set_theme(new_mode)
        st.rerun()

    # Language selector
    langs = all_langs()
    current = get_lang()
    try:
        idx = langs.index(current)
    except ValueError:
        idx = 0

    chosen = st.radio(
        t("sidebar.language"),
        options=langs,
        index=idx,
        format_func=lang_label,
        key="lang_radio_sidebar",
    )
    if chosen != current:
        set_lang(chosen)
        cm.set_language(chosen)
        st.rerun()


def _render_plugins(registry: PluginRegistry) -> None:
    """Λίστα plugins ομαδοποιημένα ανά category."""

    plugins = registry.all()

    if not plugins:
        st.markdown(
            '<div class="d4u-empty">Δεν υπάρχουν plugins ακόμα</div>',
            unsafe_allow_html=True,
        )
        return

    # Group by category
    by_category: Dict[str, List] = {}
    for p in plugins:
        cat = p.manifest.category or "General"
        by_category.setdefault(cat, []).append(p)

    # Sort categories alphabetically, plugins by name
    for cat in sorted(by_category.keys()):
        plugins_in_cat = sorted(by_category[cat], key=lambda x: x.manifest.name)

        st.markdown(
            f'<div class="d4u-category">{cat}</div>',
            unsafe_allow_html=True,
        )

        for plugin in plugins_in_cat:
            icon = plugin.manifest.icon or "🔌"
            name = plugin.manifest.name
            is_active = st.session_state.active_plugin == name
            prefix = "▶" if is_active else "  "
            label = f"{prefix} {icon} {name}"

            if st.button(
                label,
                key=f"plugin_btn_{name}",
                use_container_width=True,
            ):
                set_active_plugin(name)
                st.rerun()


def _render_errors(registry: PluginRegistry) -> None:
    """Αν υπάρχουν σπασμένα plugins, δείξε τα collapsed."""
    errors = registry.get_errors()
    if not errors:
        return

    with st.expander(f"⚠️ {len(errors)} σφάλματα", expanded=False):
        for folder, err in errors.items():
            st.caption(f"**{folder}**: {err[:120]}...")


def _render_footer() -> None:
    st.markdown(
        '<div class="d4u-sidebar-footer">'
        f'v0.1 • {t("app.tagline")}'
        '</div>',
        unsafe_allow_html=True,
    )


# ---------- Public API ----------

def render_sidebar(registry: Optional[PluginRegistry] = None) -> None:
    """Render του sidebar.

    Args:
        registry: PluginRegistry instance. Αν None → δεν δείχνει plugins.
    """
    _init_state()

    apply_theme(st.session_state.theme_mode)
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        _render_header()
        _render_controls()
        st.markdown("---")

        if registry is not None:
            _render_plugins(registry)
            _render_errors(registry)
        else:
            st.markdown(
                '<div class="d4u-empty">Δεν έχει φορτωθεί registry</div>',
                unsafe_allow_html=True,
            )

        _render_footer()