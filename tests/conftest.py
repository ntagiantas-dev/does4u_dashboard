"""Shared fixtures για όλα τα tests."""

import sys
from pathlib import Path

import pytest

# Προσθήκη του project root στο sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_yaml():
    """Ένα valid plugin manifest YAML."""
    return '''
name: test_plugin
version: 1.0.0
description: Test plugin
category: Test
icon: 🧪
requires:
  llm: false
  internet: false
tools:
  - name: hello
    description: Λέει γεια
    parameters:
      - name: name
        type: string
        description: Όνομα
        required: true
    returns:
      type: string
      description: Greeting
'''


@pytest.fixture
def temp_config(tmp_path, monkeypatch):
    """Redirect του config_manager.CONFIG_FILE σε temp path.

    ΔΕΝ αγγίζει το production ~/.does4u/.

    ΣΗΜΕΙΩΣΗ: ΔΕΝ κάνουμε mkdir εδώ — το _ensure_dir() του
    config_manager θα δημιουργήσει τον φάκελο με 0700 όταν
    πρωτογραφτεί κάτι. Αν κάναμε mkdir εδώ, ο φάκελος θα είχε
    default mode (0755) και το test_config_dir_0700 θα αποτύγχανε.
    """
    import core.config_manager as cm
    temp_dir = tmp_path / ".does4u_test"
    temp_file = temp_dir / "config.json"
    monkeypatch.setattr(cm, "CONFIG_DIR", temp_dir)
    monkeypatch.setattr(cm, "CONFIG_FILE", temp_file)
    return temp_file
