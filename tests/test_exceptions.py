"""Tests για core/exceptions.py."""

import pytest

from core.exceptions import (
    Does4uError,
    PluginError,
    ManifestError,
    PluginLoadError,
    ToolNotFoundError,
    ToolExecutionError,
    ConfigError,
)


class TestHierarchy:
    def test_does4u_is_exception(self):
        assert issubclass(Does4uError, Exception)

    def test_plugin_is_does4u(self):
        assert issubclass(PluginError, Does4uError)

    def test_manifest_is_plugin(self):
        assert issubclass(ManifestError, PluginError)

    def test_plugin_load_is_plugin(self):
        assert issubclass(PluginLoadError, PluginError)

    def test_tool_not_found_is_plugin(self):
        assert issubclass(ToolNotFoundError, PluginError)

    def test_tool_execution_is_plugin(self):
        assert issubclass(ToolExecutionError, PluginError)

    def test_config_is_does4u(self):
        assert issubclass(ConfigError, Does4uError)


class TestCatching:
    def test_catch_all_as_does4u(self):
        with pytest.raises(Does4uError):
            raise ManifestError("test")

    def test_catch_all_as_plugin(self):
        with pytest.raises(PluginError):
            raise ToolNotFoundError("test")

    def test_message_preserved(self):
        try:
            raise ManifestError("hello world")
        except ManifestError as e:
            assert str(e) == "hello world"
