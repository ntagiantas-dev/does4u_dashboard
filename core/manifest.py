"""Manifest parser: YAML → PluginManifest dataclass.

Διαβάζει ένα plugin.yaml αρχείο και επιστρέφει ένα πλήρες
PluginManifest που μπορούν να χρησιμοποιήσουν:
- το registry (TASK 1.5)
- το UI (για rendering)
- ο ntad (για MCP tools)
"""

from pathlib import Path
from typing import Any, Dict, List

import yaml

from core.exceptions import ManifestError
from core.types import PluginManifest, ToolDefinition, ToolParameter


REQUIRED_TOP_LEVEL = ("name", "tools")


def _require(data: Dict[str, Any], key: str, context: str = "") -> Any:
    """Βοηθητική: απαιτεί ένα key, αλλιώς ManifestError."""
    if key not in data:
        where = f" στο {context}" if context else ""
        raise ManifestError(f"Λείπει υποχρεωτικό πεδίο '{key}'{where}")
    return data[key]


def _parse_parameter(raw: Dict[str, Any], tool_name: str) -> ToolParameter:
    """Μετατρέπει ένα dict από το YAML σε ToolParameter."""
    if not isinstance(raw, dict):
        raise ManifestError(
            f"Το parameter στο tool '{tool_name}' δεν είναι dict: {raw!r}"
        )

    name = _require(raw, "name", f"parameter του tool '{tool_name}'")

    try:
        return ToolParameter(
            name=name,
            type=raw.get("type", "string"),
            description=raw.get("description", ""),
            required=bool(raw.get("required", True)),
            default=raw.get("default"),
        )
    except ValueError as e:
        raise ManifestError(f"Σφάλμα στο parameter '{name}': {e}")


def _parse_tool(raw: Dict[str, Any]) -> ToolDefinition:
    """Μετατρέπει ένα dict από το YAML σε ToolDefinition."""
    if not isinstance(raw, dict):
        raise ManifestError(f"Το tool δεν είναι dict: {raw!r}")

    name = _require(raw, "name", "tool")

    params_raw = raw.get("parameters", [])
    if not isinstance(params_raw, list):
        raise ManifestError(f"Τα parameters του '{name}' δεν είναι λίστα")

    parameters = [_parse_parameter(p, name) for p in params_raw]

    returns_raw = raw.get("returns", {}) or {}
    returns_type = returns_raw.get("type", "string") if isinstance(returns_raw, dict) else "string"
    returns_desc = returns_raw.get("description", "") if isinstance(returns_raw, dict) else ""

    return ToolDefinition(
        name=name,
        description=raw.get("description", ""),
        parameters=parameters,
        returns_type=returns_type,
        returns_description=returns_desc,
    )


def parse_manifest_text(text: str, source: str = "<string>") -> PluginManifest:
    """Parses YAML text → PluginManifest.

    Χρήσιμο για testing χωρίς file system.
    """
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ManifestError(f"Σφάλμα YAML στο {source}: {e}")

    if not isinstance(data, dict):
        raise ManifestError(f"Το manifest στο {source} δεν είναι dict")

    for key in REQUIRED_TOP_LEVEL:
        _require(data, key, source)

    tools_raw = data.get("tools", [])
    if not isinstance(tools_raw, list) or not tools_raw:
        raise ManifestError(f"Το 'tools' στο {source} πρέπει να είναι μη κενή λίστα")

    tools = [_parse_tool(t) for t in tools_raw]

    # Έλεγχος για διπλότυπα tool names
    names = [t.name for t in tools]
    duplicates = {n for n in names if names.count(n) > 1}
    if duplicates:
        raise ManifestError(f"Διπλότυπα tools στο {source}: {sorted(duplicates)}")

    requires = data.get("requires", {}) or {}
    if not isinstance(requires, dict):
        raise ManifestError(f"Το 'requires' στο {source} πρέπει να είναι dict")

    return PluginManifest(
        name=data["name"],
        version=str(data.get("version", "0.1.0")),
        description=data.get("description", ""),
        category=data.get("category", "General"),
        author=data.get("author", "does4u"),
        icon=data.get("icon", "🔌"),
        color=data.get("color", "#1F4E79"),
        requires_llm=bool(requires.get("llm", False)),
        requires_internet=bool(requires.get("internet", False)),
        tools=tools,
    )


def parse_manifest_file(path: Path) -> PluginManifest:
    """Διαβάζει ένα plugin.yaml από το δίσκο → PluginManifest."""
    path = Path(path)
    if not path.exists():
        raise ManifestError(f"Το manifest δεν υπάρχει: {path}")
    if not path.is_file():
        raise ManifestError(f"Το manifest δεν είναι αρχείο: {path}")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise ManifestError(f"Σφάλμα ανάγνωσης {path}: {e}")

    return parse_manifest_text(text, source=str(path))
