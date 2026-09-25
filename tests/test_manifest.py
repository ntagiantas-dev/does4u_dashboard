"""Tests για core/manifest.py."""

import pytest

from core.exceptions import ManifestError
from core.manifest import parse_manifest_text, parse_manifest_file


class TestParseText:
    def test_valid(self, sample_yaml):
        m = parse_manifest_text(sample_yaml)
        assert m.name == "test_plugin"
        assert m.version == "1.0.0"
        assert m.icon == "🧪"
        assert len(m.tools) == 1
        assert m.tools[0].name == "hello"

    def test_missing_name(self):
        with pytest.raises(ManifestError, match="name"):
            parse_manifest_text("tools:\n  - name: x\n    description: y")

    def test_missing_tools(self):
        with pytest.raises(ManifestError, match="tools"):
            parse_manifest_text("name: test")

    def test_empty_tools(self):
        with pytest.raises(ManifestError):
            parse_manifest_text("name: test\ntools: []")

    def test_duplicate_tool_names(self):
        y = """
name: test
tools:
  - name: x
    description: a
  - name: x
    description: b
"""
        with pytest.raises(ManifestError, match="Διπλότυπα"):
            parse_manifest_text(y)

    def test_invalid_param_type(self):
        y = """
name: test
tools:
  - name: x
    description: a
    parameters:
      - name: p
        type: banana
"""
        with pytest.raises(ManifestError):
            parse_manifest_text(y)

    def test_invalid_yaml(self):
        with pytest.raises(ManifestError, match="YAML"):
            parse_manifest_text("name: test\n  bad indent: :")

    def test_non_dict_top_level(self):
        with pytest.raises(ManifestError):
            parse_manifest_text("- item1\n- item2")

    def test_requires_defaults(self):
        y = """
name: test
tools:
  - name: x
    description: y
"""
        m = parse_manifest_text(y)
        assert m.requires_llm is False
        assert m.requires_internet is False

    def test_requires_set(self, sample_yaml):
        y = sample_yaml.replace("llm: false", "llm: true").replace(
            "internet: false", "internet: true"
        )
        m = parse_manifest_text(y)
        assert m.requires_llm is True
        assert m.requires_internet is True

    def test_param_defaults(self, sample_yaml):
        m = parse_manifest_text(sample_yaml)
        p = m.tools[0].get_parameter("name")
        assert p is not None
        assert p.type == "string"
        assert p.required is True


class TestParseFile:
    def test_missing_file(self, tmp_path):
        with pytest.raises(ManifestError, match="δεν υπάρχει"):
            parse_manifest_file(tmp_path / "nope.yaml")

    def test_directory_instead_of_file(self, tmp_path):
        with pytest.raises(ManifestError):
            parse_manifest_file(tmp_path)

    def test_valid_file(self, tmp_path, sample_yaml):
        f = tmp_path / "plugin.yaml"
        f.write_text(sample_yaml, encoding="utf-8")
        m = parse_manifest_file(f)
        assert m.name == "test_plugin"
