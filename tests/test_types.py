"""Tests για core/types.py."""

import pytest

from core.types import (
    ToolParameter,
    ToolDefinition,
    PluginManifest,
    ToolResult,
    VALID_PARAM_TYPES,
)


class TestToolParameter:
    def test_basic(self):
        p = ToolParameter(name="x", type="string", description="test")
        assert p.name == "x"
        assert p.type == "string"
        assert p.required is True

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            ToolParameter(name="x", type="banana")

    def test_all_valid_types(self):
        for t in VALID_PARAM_TYPES:
            p = ToolParameter(name="x", type=t)
            assert p.type == t

    def test_optional(self):
        p = ToolParameter(name="x", type="string", required=False, default="hi")
        assert p.required is False
        assert p.default == "hi"

    def test_to_mcp_schema(self):
        p = ToolParameter(name="x", type="number", description="a number")
        s = p.to_mcp_schema()
        assert s["type"] == "number"
        assert s["description"] == "a number"

    def test_to_mcp_schema_with_default(self):
        p = ToolParameter(name="x", type="integer", default=5)
        s = p.to_mcp_schema()
        assert s["default"] == 5


class TestToolDefinition:
    def test_basic(self):
        t = ToolDefinition(name="calc", description="calc")
        assert t.name == "calc"
        assert t.parameters == []

    def test_get_parameter(self):
        p1 = ToolParameter(name="a")
        p2 = ToolParameter(name="b")
        t = ToolDefinition(name="x", description="", parameters=[p1, p2])
        assert t.get_parameter("a") is p1
        assert t.get_parameter("b") is p2
        assert t.get_parameter("c") is None

    def test_to_mcp_schema(self):
        p1 = ToolParameter(name="a", type="number", required=True)
        p2 = ToolParameter(name="b", type="string", required=False)
        t = ToolDefinition(name="calc", description="calc", parameters=[p1, p2])
        s = t.to_mcp_schema()
        assert s["name"] == "calc"
        assert "inputSchema" in s
        assert s["inputSchema"]["type"] == "object"
        assert "a" in s["inputSchema"]["properties"]
        assert "b" in s["inputSchema"]["properties"]
        assert s["inputSchema"]["required"] == ["a"]

    def test_to_mcp_no_required(self):
        p = ToolParameter(name="a", required=False)
        t = ToolDefinition(name="x", description="", parameters=[p])
        s = t.to_mcp_schema()
        assert "required" not in s["inputSchema"]


class TestPluginManifest:
    def test_basic(self):
        m = PluginManifest(name="test")
        assert m.name == "test"
        assert m.version == "0.1.0"
        assert m.tools == []

    def test_get_tool(self):
        t1 = ToolDefinition(name="a", description="")
        t2 = ToolDefinition(name="b", description="")
        m = PluginManifest(name="x", tools=[t1, t2])
        assert m.get_tool("a") is t1
        assert m.get_tool("b") is t2
        assert m.get_tool("c") is None

    def test_to_mcp_tools(self):
        t = ToolDefinition(name="foo", description="")
        m = PluginManifest(name="x", tools=[t])
        schemas = m.to_mcp_tools()
        assert len(schemas) == 1
        assert schemas[0]["name"] == "foo"


class TestToolResult:
    def test_ok(self):
        r = ToolResult.ok(data=42, unit="EUR")
        assert r.success is True
        assert r.data == 42
        assert r.error is None
        assert r.metadata["unit"] == "EUR"

    def test_fail(self):
        r = ToolResult.fail(error="boom", code=500)
        assert r.success is False
        assert r.data is None
        assert r.error == "boom"
        assert r.metadata["code"] == 500

    def test_ok_no_data(self):
        r = ToolResult.ok()
        assert r.success is True
        assert r.data is None
