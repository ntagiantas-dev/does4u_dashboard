"""Abstract base class για όλα τα plugins του does4u Dashboard.

Κάθε plugin:
- Κληρονομεί από το BasePlugin
- Υλοποιεί τη run_tool()
- Αποκτά manifest μέσω του registry (TASK 1.5)

MCP-ready: το BasePlugin εκθέτει list_tools() και
execute() που μπορούν να κληθούν από MCP host ή από τον ntad.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.exceptions import PluginError, ToolNotFoundError
from core.types import PluginManifest, ToolDefinition, ToolResult


class BasePlugin(ABC):
    """Abstract base για όλα τα plugins."""

    def __init__(self):
        self._manifest: Optional[PluginManifest] = None

    @property
    def manifest(self) -> PluginManifest:
        if self._manifest is None:
            raise PluginError(
                f"Το manifest δεν έχει φορτωθεί για το {self.__class__.__name__}. "
                "Χρησιμοποίησε attach_manifest() πρώτα."
            )
        return self._manifest

    def attach_manifest(self, manifest: PluginManifest) -> None:
        """Καλείται από το registry μετά τη φόρτωση."""
        self._manifest = manifest

    @property
    def name(self) -> str:
        return self.manifest.name

    def list_tools(self) -> List[ToolDefinition]:
        """Επιστρέφει όλα τα tools του plugin."""
        return self.manifest.tools

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Επιστρέφει ένα tool by name ή None."""
        return self.manifest.get_tool(name)

    def to_mcp_tools(self) -> List[Dict[str, Any]]:
        """Επιστρέφει όλα τα tools σε MCP format."""
        return self.manifest.to_mcp_tools()

    @abstractmethod
    def run_tool(self, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """Εκτελεί ένα tool με τις δοσμένες παραμέτρους."""
        ...

    def execute(self, tool_name: str, params: Optional[Dict[str, Any]] = None) -> ToolResult:
        """Public API για εκτέλεση tool."""
        if params is None:
            params = {}

        tool = self.get_tool(tool_name)
        if tool is None:
            raise ToolNotFoundError(
                f"Το tool '{tool_name}' δεν υπάρχει στο plugin '{self.name}'"
            )

        missing = []
        for p in tool.parameters:
            if p.required and p.name not in params:
                missing.append(p.name)

        if missing:
            return ToolResult.fail(
                f"Λείπουν υποχρεωτικές παράμετροι: {', '.join(missing)}"
            )

        return self.run_tool(tool_name, params)

    def info(self) -> Dict[str, Any]:
        """Σύνοψη του plugin."""
        if self._manifest is None:
            return {"name": self.__class__.__name__, "loaded": False}
        return {
            "name": self.manifest.name,
            "version": self.manifest.version,
            "description": self.manifest.description,
            "category": self.manifest.category,
            "icon": self.manifest.icon,
            "tools": [t.name for t in self.manifest.tools],
            "loaded": True,
        }

    def __repr__(self) -> str:
        try:
            return f"<{self.__class__.__name__} name={self.manifest.name}>"
        except PluginError:
            return f"<{self.__class__.__name__} (no manifest)>"
