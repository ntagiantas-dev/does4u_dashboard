"""Tests για core/plugin_registry.py."""

import pytest

from core.exceptions import PluginError
from core.plugin_registry import PluginRegistry


PLUGIN_YAML = """
name: {name}
version: 1.0.0
description: test
category: Test
tools:
  - name: hello
    description: y
    parameters: []
"""

PLUGIN_PY = """
from core.plugin_base import BasePlugin
from core.types import ToolResult

class Plugin(BasePlugin):
    def run_tool(self, tool_name, params):
        return ToolResult.ok(data="ok")
"""


def make_plugin(root, folder, name):
    d = root / folder
    d.mkdir()
    (d / "__init__.py").write_text("")
    (d / "plugin.yaml").write_text(PLUGIN_YAML.format(name=name))
    (d / "plugin.py").write_text(PLUGIN_PY)
    return d


class TestDiscovery:
    def test_empty_dir(self, tmp_path):
        reg = PluginRegistry(tmp_path)
        assert reg.discover() == []

    def test_nonexistent_dir(self, tmp_path):
        reg = PluginRegistry(tmp_path / "nope")
        assert reg.discover() == []

    def test_finds_plugin(self, tmp_path):
        make_plugin(tmp_path, "one", "one")
        reg = PluginRegistry(tmp_path)
        assert len(reg.discover()) == 1

    def test_ignores_hidden(self, tmp_path):
        make_plugin(tmp_path, ".hidden", "h")
        reg = PluginRegistry(tmp_path)
        assert reg.discover() == []

    def test_ignores_non_plugin_folders(self, tmp_path):
        d = tmp_path / "notaplugin"
        d.mkdir()
        (d / "readme.txt").write_text("hi")
        reg = PluginRegistry(tmp_path)
        assert reg.discover() == []


class TestLoading:
    def test_load_all_empty(self, tmp_path):
        reg = PluginRegistry(tmp_path)
        result = reg.load_all()
        assert result["total_loaded"] == 0
        assert result["total_failed"] == 0

    def test_load_two(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        make_plugin(tmp_path, "b", "b")
        reg = PluginRegistry(tmp_path)
        result = reg.load_all()
        assert result["total_loaded"] == 2
        assert sorted(result["loaded"]) == ["a", "b"]
        assert reg.count() == 2

    def test_broken_yaml_doesnt_kill(self, tmp_path):
        make_plugin(tmp_path, "good", "good")
        bad = tmp_path / "bad"
        bad.mkdir()
        (bad / "__init__.py").write_text("")
        (bad / "plugin.yaml").write_text("!!!invalid:::")
        (bad / "plugin.py").write_text("class Plugin: pass")
        reg = PluginRegistry(tmp_path)
        result = reg.load_all()
        assert result["total_loaded"] == 1
        assert result["total_failed"] == 1

    def test_duplicate_name(self, tmp_path):
        make_plugin(tmp_path, "folder1", "same")
        make_plugin(tmp_path, "folder2", "same")
        reg = PluginRegistry(tmp_path)
        result = reg.load_all()
        assert result["total_loaded"] == 1
        assert result["total_failed"] == 1


class TestAccess:
    def test_get_and_has(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        assert reg.has("a") is True
        assert reg.has("nope") is False
        assert reg.get("a") is not None
        assert reg.get("nope") is None

    def test_get_or_raise(self, tmp_path):
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        with pytest.raises(PluginError):
            reg.get_or_raise("nope")

    def test_names_sorted(self, tmp_path):
        make_plugin(tmp_path, "b", "b")
        make_plugin(tmp_path, "a", "a")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        assert reg.names() == ["a", "b"]

    def test_all(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        assert len(reg.all()) == 1

    def test_get_errors(self, tmp_path):
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        assert reg.get_errors() == {}


class TestMCP:
    def test_list_all_tools(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        make_plugin(tmp_path, "b", "b")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        tools = reg.list_all_tools()
        assert len(tools) == 2
        assert all("plugin" in t and "tool" in t for t in tools)

    def test_execute(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        r = reg.execute("a", "hello", {})
        assert r.success is True

    def test_execute_missing_plugin(self, tmp_path):
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        with pytest.raises(PluginError):
            reg.execute("nope", "x", {})

    def test_summary(self, tmp_path):
        make_plugin(tmp_path, "a", "a")
        reg = PluginRegistry(tmp_path)
        reg.load_all()
        s = reg.summary()
        assert "a" in s
        assert "Loaded" in s
