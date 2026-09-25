"""does4u Dashboard — entry point.

Flow:
1. set_page_config
2. Init session state (theme/lang από config_manager)
3. Onboarding check → αν χρειάζεται, render, STOP
4. Φόρτωση plugins από registry
5. Render sidebar
6. Render plugin page ή home
"""

from pathlib import Path

import streamlit as st

from config.theme import apply_theme, DEFAULT_THEME
from config.i18n import get_lang, set_lang
from core import config_manager as cm
from core.plugin_registry import PluginRegistry
from ui.onboarding import render_onboarding, is_onboarding_needed
from ui.sidebar import render_sidebar, get_active_plugin, set_active_plugin
from ui.plugin_page import render_plugin_page
from ui.home import render_home


PLUGINS_DIR = Path(__file__).parent / "plugins"


# ---------- Page config ----------

st.set_page_config(
    page_title="does4u Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- Session state init ----------

def _init_session() -> None:
    """Συγχρονίζει session_state με το persisted config."""
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = cm.get_theme() or DEFAULT_THEME
    if "lang" not in st.session_state:
        st.session_state.lang = cm.get_language() or get_lang()
    if "active_plugin" not in st.session_state:
        st.session_state.active_plugin = None


_init_session()


# ---------- Onboarding gate ----------

if is_onboarding_needed():
    render_onboarding()
    st.stop()


# ---------- Apply theme ----------

apply_theme(st.session_state.theme_mode)


# ---------- Load plugins ----------

@st.cache_resource(show_spinner=False)
def _get_registry() -> PluginRegistry:
    """Φορτώνει τα plugins ΜΙΑ φορά (cache).

    Για refresh κατά την ανάπτυξη: Ctrl+C + restart streamlit.
    """
    reg = PluginRegistry(PLUGINS_DIR)
    reg.load_all()
    return reg


registry = _get_registry()


# ---------- Sidebar ----------

render_sidebar(registry)


# ---------- Main content ----------

active_name = get_active_plugin()

if active_name is None:
    render_home(registry)
else:
    plugin = registry.get(active_name)
    if plugin is None:
        # Το plugin υπήρχε αλλά εξαφανίστηκε (π.χ. σβήστηκε ο φάκελος)
        set_active_plugin(None)
        render_home(registry)
    else:
        render_plugin_page(plugin)