"""Tests για core/config_manager.py."""

import json
import os

import pytest

from core import config_manager as cm
from core.exceptions import ConfigError


class TestDefaults:
    def test_get_config_defaults(self, temp_config):
        cfg = cm.get_config()
        assert cfg["version"] == "1.0"
        assert cfg["onboarding_completed"] is False
        assert cfg["language"] == "el"
        assert cfg["theme"] == "dark"
        assert "openai" in cfg["providers"]
        assert "anthropic" in cfg["providers"]
        assert "xai" in cfg["providers"]

    def test_config_file_not_created_on_read(self, temp_config):
        cm.get_config()
        assert not temp_config.exists()


class TestOnboarding:
    def test_initially_not_completed(self, temp_config):
        assert cm.is_onboarding_completed() is False

    def test_mark_completed(self, temp_config):
        cm.mark_onboarding_completed()
        assert cm.is_onboarding_completed() is True


class TestApiKeys:
    def test_empty_initially(self, temp_config):
        assert cm.get_api_key("openai") == ""
        assert cm.has_api_key("openai") is False

    def test_set_and_get(self, temp_config):
        cm.set_api_key("openai", "sk-test")
        assert cm.get_api_key("openai") == "sk-test"
        assert cm.has_api_key("openai") is True

    def test_whitespace_stripped(self, temp_config):
        cm.set_api_key("openai", "  sk-xx  ")
        assert cm.get_api_key("openai") == "sk-xx"

    def test_unknown_provider(self, temp_config):
        with pytest.raises(ConfigError):
            cm.set_api_key("nope", "x")

    def test_non_string_key(self, temp_config):
        with pytest.raises(ConfigError):
            cm.set_api_key("openai", 123)


class TestProvider:
    def test_default_active(self, temp_config):
        assert cm.get_active_provider() == "openai"

    def test_set_active(self, temp_config):
        cm.set_active_provider("anthropic")
        assert cm.get_active_provider() == "anthropic"

    def test_unknown_provider(self, temp_config):
        with pytest.raises(ConfigError):
            cm.set_active_provider("nope")

    def test_default_model(self, temp_config):
        assert cm.get_default_model("openai") == "gpt-4o-mini"

    def test_set_model(self, temp_config):
        cm.set_default_model("openai", "gpt-4o")
        assert cm.get_default_model("openai") == "gpt-4o"


class TestLanguageTheme:
    def test_defaults(self, temp_config):
        assert cm.get_language() == "el"
        assert cm.get_theme() == "dark"

    def test_set(self, temp_config):
        cm.set_language("en")
        cm.set_theme("light")
        assert cm.get_language() == "en"
        assert cm.get_theme() == "light"


class TestPersistence:
    def test_reload(self, temp_config):
        cm.set_api_key("openai", "sk-persist")
        cm.set_language("en")
        cm.mark_onboarding_completed()
        assert cm.get_api_key("openai") == "sk-persist"
        assert cm.get_language() == "en"
        assert cm.is_onboarding_completed() is True


class TestFilesystem:
    def test_permissions_600(self, temp_config):
        cm.set_language("en")
        mode = oct(os.stat(temp_config).st_mode)[-3:]
        assert mode == "600"

    def test_config_dir_0700(self, temp_config):
        cm.set_language("en")
        dir_mode = oct(os.stat(temp_config.parent).st_mode)[-3:]
        assert dir_mode == "700"


class TestCorrupted:
    def test_corrupted_json_falls_back(self, temp_config):
        temp_config.parent.mkdir(parents=True, exist_ok=True)
        temp_config.write_text("{ invalid json ]]")
        cfg = cm.get_config()
        assert cfg["version"] == "1.0"
        assert cm.get_language() == "el"

    def test_corrupted_backup_created(self, temp_config):
        temp_config.parent.mkdir(parents=True, exist_ok=True)
        temp_config.write_text("not json")
        cm.get_config()
        backup = temp_config.with_suffix(".json.corrupted")
        assert backup.exists()


class TestReset:
    def test_reset(self, temp_config):
        cm.set_language("en")
        cm.reset_config()
        assert not temp_config.exists()
        assert cm.get_language() == "el"

    def test_reset_nonexistent(self, temp_config):
        cm.reset_config()
