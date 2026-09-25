"""Plugin page — generic renderer για plugins.

Δείχνει τη σελίδα ενός plugin. ΔΕΝ ξέρει τι κάνει το plugin —
όλα από το manifest + το execute() API.

Hybrid:
- Αν το plugin έχει render_ui() → custom
- Αλλιώς → auto-form από τα tools (tabs)

Public API:
- render_plugin_page(plugin) → None
- render_empty_state() → None
"""

from typing import Any, Dict, Optional

import streamlit as st

from config.i18n import t
from core.plugin_base import BasePlugin
from core.types import ToolDefinition, ToolParameter, ToolResult


PLUGIN_PAGE_CSS = """
<style>
.d4u-plugin-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    margin-bottom: 1.5rem;
}
.d4u-plugin-icon {
    font-size: 2.5rem;
    line-height: 1;
}
.d4u-plugin-title-block {
    flex: 1;
}
.d4u-plugin-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
    line-height: 1.2;
}
.d4u-plugin-desc {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin: 0.2rem 0 0 0;
}
.d4u-plugin-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: right;
    white-space: nowrap;
}
.d4u-plugin-meta code {
    background: var(--surface-2);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    font-size: 0.7rem;
    color: var(--text);
}

.d4u-empty-state {
    text-align: center;
    padding: 4rem 1rem;
    color: var(--text-muted);
}
.d4u-empty-state-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.4;
}
.d4u-empty-state-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 0.5rem;
}

.d4u-result-box {
    padding: 1rem 1.25rem;
    border-radius: var(--radius-sm);
    margin-top: 1rem;
    border: 1px solid var(--border);
    background: var(--surface);
}
.d4u-result-box.success {
    border-left: 4px solid var(--success);
}
.d4u-result-box.error {
    border-left: 4px solid var(--error);
}
.d4u-result-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

.d4u-param-hint {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}
</style>
"""


# ---------- State ----------

def _state_key(plugin_name: str, tool_name: str, param_name: str) -> str:
    return f"pform_{plugin_name}_{tool_name}_{param_name}"


def _get_param_value(plugin_name: str, tool_name: str, param: ToolParameter) -> Any:
    key = _state_key(plugin_name, tool_name, param.name)
    if key in st.session_state:
        return st.session_state[key]
    return param.default


def _clear_form(plugin_name: str) -> None:
    """Καθαρίζει όλα τα inputs του plugin."""
    prefix = f"pform_{plugin_name}_"
    for k in list(st.session_state.keys()):
        if k.startswith(prefix):
            del st.session_state[k]


# ---------- Rendering: Header ----------

def _render_header(plugin: BasePlugin) -> None:
    m = plugin.manifest
    icon = m.icon or "🔌"
    version = m.version or "?"
    author = m.author or "?"
    category = m.category or "General"

    st.markdown(
        f'<div class="d4u-plugin-header">'
        f'  <div class="d4u-plugin-icon">{icon}</div>'
        f'  <div class="d4u-plugin-title-block">'
        f'    <div class="d4u-plugin-title">{m.name}</div>'
        f'    <div class="d4u-plugin-desc">{m.description or ""}</div>'
        f'  </div>'
        f'  <div class="d4u-plugin-meta">'
        f'    v{version}<br>{t("plugin.by")} {author}<br>'
        f'    <code>{category}</code>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------- Rendering: Empty state ----------

def render_empty_state() -> None:
    """Δείχνεται όταν δεν έχει επιλεγεί plugin."""
    st.markdown(
        f'<div class="d4u-empty-state">'
        f'  <div class="d4u-empty-state-icon">🎯</div>'
        f'  <div class="d4u-empty-state-title">{t("plugin.no_selection")}</div>'
        f'  <div>{t("plugin.no_selection_hint")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------- Rendering: Result ----------

def _render_result(result: ToolResult) -> None:
    if result.success:
        st.markdown(
            f'<div class="d4u-result-box success">'
            f'<div class="d4u-result-label">✅ {t("plugin.result")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        _render_data(result.data)
    else:
        st.markdown(
            f'<div class="d4u-result-box error">'
            f'<div class="d4u-result-label">❌ {t("plugin.error")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.error(result.error or "Unknown error")

    # Metadata (αν υπάρχει)
    if result.metadata:
        with st.expander("Metadata", expanded=False):
            st.json(result.metadata)


def _render_data(data: Any) -> None:
    """Auto-detect το format και δείξε το κατάλληλα."""
    if data is None:
        st.caption("(κενό αποτέλεσμα)")
    elif isinstance(data, (dict, list)):
        st.json(data)
    elif isinstance(data, str):
        if data.strip():
            st.markdown(data)
        else:
            st.caption("(κενό string)")
    elif isinstance(data, bool):
        st.write("✅ Ναι" if data else "❌ Όχι")
    else:
        st.write(data)


# ---------- Rendering: Inputs ----------

def _render_input(plugin_name: str, tool_name: str, param: ToolParameter) -> None:
    """Ένα input ανάλογα με τον τύπο του parameter."""
    key = _state_key(plugin_name, tool_name, param.name)
    label = param.name
    if param.required:
        label += " *"
    if param.description:
        st.markdown(
            f'<div class="d4u-param-hint">{param.description}</div>',
            unsafe_allow_html=True,
        )

    ptype = param.type
    default = param.default

    if ptype == "number":
        st.number_input(
            label,
            value=float(default) if isinstance(default, (int, float)) else 0.0,
            step=1.0,
            format="%.4f",
            key=key,
        )
    elif ptype == "integer":
        st.number_input(
            label,
            value=int(default) if isinstance(default, int) else 0,
            step=1,
            key=key,
        )
    elif ptype == "boolean":
        st.checkbox(
            label,
            value=bool(default) if default is not None else False,
            key=key,
        )
    elif ptype == "array":
        raw = st.text_area(
            label + " (μία τιμή ανά γραμμή)",
            value="\n".join(str(x) for x in (default or [])),
            key=key,
        )
    elif ptype == "object":
        raw = st.text_area(
            label + " (JSON)",
            value=default if isinstance(default, str) else "{}",
            key=key,
        )
    else:  # string
        st.text_input(
            label,
            value=str(default) if default is not None else "",
            key=key,
        )


def _collect_params(plugin_name: str, tool: ToolDefinition) -> Dict[str, Any]:
    """Διαβάζει τις τιμές από το session_state."""
    params: Dict[str, Any] = {}
    for p in tool.parameters:
        key = _state_key(plugin_name, tool.name, p.name)
        raw = st.session_state.get(key, p.default)

        # Coercion για array/object
        if p.type == "array" and isinstance(raw, str):
            raw = [line for line in raw.split("\n") if line.strip()]
        elif p.type == "object" and isinstance(raw, str):
            import json
            try:
                raw = json.loads(raw) if raw.strip() else {}
            except json.JSONDecodeError:
                raw = {}

        params[p.name] = raw
    return params


# ---------- Rendering: Tool tab ----------

def _render_tool_tab(plugin: BasePlugin, tool: ToolDefinition) -> None:
    """Περιεχόμενο ενός tab — inputs + execute button + result."""

    # Inputs
    if tool.parameters:
        for p in tool.parameters:
            _render_input(plugin.manifest.name, tool.name, p)
    else:
        st.caption("Το tool δεν έχει παραμέτρους.")

    st.markdown("")

    # Buttons
    col1, col2, _ = st.columns([1, 1, 4])
    with col1:
        run_clicked = st.button(
            t("plugin.execute"),
            key=f"run_{plugin.manifest.name}_{tool.name}",
            type="primary",
            use_container_width=True,
        )
    with col2:
        clear_clicked = st.button(
            t("plugin.reset"),
            key=f"clear_{plugin.manifest.name}_{tool.name}",
            use_container_width=True,
        )

    if clear_clicked:
        _clear_form(plugin.manifest.name)
        st.rerun()

    if run_clicked:
        params = _collect_params(plugin.manifest.name, tool)
        try:
            with st.spinner(t("plugin.executing")):
                result = plugin.execute(tool.name, params)
        except Exception as e:
            result = ToolResult.fail(error=f"Exception: {e}")
        _render_result(result)


# ---------- Rendering: Auto-form ----------

def _render_auto_form(plugin: BasePlugin) -> None:
    """Auto-form με tabs, ένα tab ανά tool."""
    tools = plugin.list_tools()

    if not tools:
        st.info(t("plugin.no_tools"))
        return

    if len(tools) == 1:
        _render_tool_tab(plugin, tools[0])
        return

    tab_labels = [f"{tool.name}" for tool in tools]
    tabs = st.tabs(tab_labels)
    for tab, tool in zip(tabs, tools):
        with tab:
            _render_tool_tab(plugin, tool)


# ---------- Public API ----------

def render_plugin_page(plugin: Optional[BasePlugin]) -> None:
    """Render τη σελίδα ενός plugin.

    Αν plugin is None → δείχνει empty state.
    """
    st.markdown(PLUGIN_PAGE_CSS, unsafe_allow_html=True)

    if plugin is None:
        render_empty_state()
        return

    _render_header(plugin)

    # HYBRID: custom render_ui() αν υπάρχει
    if hasattr(plugin, "render_ui") and callable(getattr(plugin, "render_ui")):
        try:
            plugin.render_ui()
            return
        except Exception as e:
            st.error(f"Σφάλμα στο custom UI: {e}")
            st.caption("Fallback σε auto-form:")
            st.markdown("---")

    _render_auto_form(plugin)