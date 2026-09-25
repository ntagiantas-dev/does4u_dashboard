"""Tests για core/plugin_base.py."""

import pytest

from core.exceptions import PluginError, ToolNotFoundError
from core.plugin_base import BasePlugin
from core.types import (
    PluginManifest,
    ToolDefinition,
    ToolParameter,
    ToolResult,
)


class DummyPlugin(BasePlugin):
    def run_tool(self, tool_name, params):
        if tool_name == "echo":
            return ToolResult.ok(data=params.get("msg", ""))
        if tool_name == "add":
            return ToolResult.ok(data=params["a"] + params["b"])
        return ToolResult.fail(error="unknown")


def make_manifest():
    t1 = ToolDefinition(
        name="echo",
        description="echo",
        parameters=[ToolParameter(name="msg", required=False)],
    )
    t2 = ToolDefinition(
        name="add",
        description="add",
        parameters=[
            ToolParameter(name="a", type="number"),
            ToolParameter(name="b", type="number"),
        ],
    )
    return PluginManifest(name="dummy", tools=[t1, t2])


class TestAbstract:
    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            BasePlugin()

    def test_must_implement_run_tool(self):
        class Incomplete(BasePlugin):
            pass
        with pytest.raises(TypeError):
            Incomplete()


class TestManifestAttach:
    def test_manifest_not_attached(self):
        p = DummyPlugin()
        with pytest.raises(PluginError):
            _ = p.manifest

    def test_attach(self):
        p = DummyPlugin()
        m = make_manifest()
        p.attach_manifest(m)
        assert p.manifest is m
        assert p.name == "dummy"

    def test_info_before_manifest(self):
        p = DummyPlugin()
        info = p.info()
        assert info["loaded"] is False

    def test_info_after_manifest(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        info = p.info()
        assert info["loaded"] is True
        assert info["name"] == "dummy"
        assert "echo" in info["tools"]


class TestTools:
    def test_list_tools(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        assert len(p.list_tools()) == 2

    def test_get_tool(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        assert p.get_tool("echo") is not None
        assert p.get_tool("nope") is None

    def test_to_mcp_tools(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        schemas = p.to_mcp_tools()
        assert len(schemas) == 2


class TestExecute:
    def test_success(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        r = p.execute("echo", {"msg": "hi"})
        assert r.success is True
        assert r.data == "hi"

    def test_add(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        r = p.execute("add", {"a": 2, "b": 3})
        assert r.data == 5

    def test_unknown_tool(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        with pytest.raises(ToolNotFoundError):
            p.execute("nope", {})

    def test_missing_required(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        r = p.execute("add", {"a": 1})
        assert r.success is False
        assert "b" in r.error

    def test_none_params(self):
        p = DummyPlugin()
        p.attach_manifest(make_manifest())
        r = p.execute("add", None)
        assert r.success is False

    def test_repr(self):
        p = DummyPlugin()
        assert "DummyPlugin" in repr(p)
        p.attach_manifest(make_manifest())
        assert "dummy" in repr(p)
