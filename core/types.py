"""Dataclasses για το plugin system.

MCP-ready: το ToolDefinition.to_mcp_schema() επιστρέφει
format συμβατό με το Model Context Protocol.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Έγκυροι τύποι παραμέτρων (MCP-compatible)
VALID_PARAM_TYPES = {"string", "number", "integer", "boolean", "object", "array"}


@dataclass
class ToolParameter:
    """Παράμετρος ενός tool."""
    name: str
    type: str = "string"
    description: str = ""
    required: bool = True
    default: Any = None

    def to_mcp_schema(self) -> Dict[str, Any]:
        """Επιστρέφει JSON Schema για την παράμετρο."""
        schema: Dict[str, Any] = {
            "type": self.type,
            "description": self.description,
        }
        if self.default is not None:
            schema["default"] = self.default
        return schema

    def __post_init__(self):
        if self.type not in VALID_PARAM_TYPES:
            raise ValueError(
                f"Μη έγκυρος τύπος παραμέτρου: {self.type}. "
                f"Έγκυροι: {sorted(VALID_PARAM_TYPES)}"
            )


@dataclass
class ToolDefinition:
    """Ορισμός ενός tool που εκθέτει ένα plugin."""
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    returns_type: str = "string"
    returns_description: str = ""

    def to_mcp_schema(self) -> Dict[str, Any]:
        """Επιστρέφει το tool σε MCP format."""
        properties = {p.name: p.to_mcp_schema() for p in self.parameters}
        required = [p.name for p in self.parameters if p.required]

        schema: Dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": properties,
            },
        }
        if required:
            schema["inputSchema"]["required"] = required
        return schema

    def get_parameter(self, name: str) -> Optional[ToolParameter]:
        for p in self.parameters:
            if p.name == name:
                return p
        return None


@dataclass
class PluginManifest:
    """Περιεχόμενο του plugin.yaml."""
    name: str
    version: str = "0.1.0"
    description: str = ""
    category: str = "General"
    author: str = "does4u"
    icon: str = "🔌"
    color: str = "#1F4E79"
    requires_llm: bool = False
    requires_internet: bool = False
    tools: List[ToolDefinition] = field(default_factory=list)

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        for t in self.tools:
            if t.name == name:
                return t
        return None

    def to_mcp_tools(self) -> List[Dict[str, Any]]:
        """Όλα τα tools του plugin σε MCP format."""
        return [t.to_mcp_schema() for t in self.tools]


@dataclass
class ToolResult:
    """Αποτέλεσμα εκτέλεσης ενός tool."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: Any = None, **metadata) -> "ToolResult":
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(cls, error: str, **metadata) -> "ToolResult":
        return cls(success=False, error=error, metadata=metadata)
