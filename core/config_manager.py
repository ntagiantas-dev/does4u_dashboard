"""Config manager για does4u Dashboard.

Διαχειρίζεται το config του χρήστη:
- Location: ~/.does4u/config.json (ΕΞΩ από το project)
- Format: JSON
- API keys: plaintext (τοπικά, με 0600 permissions)
- Atomic writes για ασφάλεια σε crashes

Public API:
- get_config() → dict
- save_config(cfg) → None
- get_api_key(provider) → str
- set_api_key(provider, key) → None
- get_active_provider() / set_active_provider()
- is_onboarding_completed() / mark_onboarding_completed()
- reset_config() → None (για testing)
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

from core.exceptions import ConfigError


CONFIG_DIR = Path.home() / ".does4u"
CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_VERSION = "1.0"


# ---------- Defaults ----------

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": CONFIG_VERSION,
    "onboarding_completed": False,
    "language": "el",
    "theme": "dark",
    "providers": {
        "openai": {
            "api_key": "",
            "default_model": "gpt-4o-mini",
        },
        "anthropic": {
            "api_key": "",
            "default_model": "claude-3-5-sonnet-20241022",
        },
        "xai": {
            "api_key": "",
            "default_model": "grok-2-latest",
        },
    },
    "active_provider": "openai",
}


def _deep_copy_defaults() -> Dict[str, Any]:
    """Επιστρέφει φρέσκο αντίγραφο των defaults."""
    return json.loads(json.dumps(DEFAULT_CONFIG))


def _merge_defaults(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Συμπληρώνει λείποντα πεδία από τα defaults (shallow + providers)."""
    merged = _deep_copy_defaults()
    for k, v in cfg.items():
        if k == "providers" and isinstance(v, dict):
            for prov, prov_cfg in v.items():
                if prov in merged["providers"] and isinstance(prov_cfg, dict):
                    merged["providers"][prov].update(prov_cfg)
                else:
                    merged["providers"][prov] = prov_cfg
        else:
            merged[k] = v
    return merged


# ---------- Filesystem ----------

def _ensure_dir() -> None:
    """Δημιουργεί το ~/.does4u/ με 0700 αν δεν υπάρχει."""
    if CONFIG_DIR.exists():
        return
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(CONFIG_DIR, 0o700)
    except OSError as e:
        raise ConfigError(f"Αδυναμία δημιουργίας {CONFIG_DIR}: {e}")


def _write_atomic(path: Path, data: Dict[str, Any]) -> None:
    """Γράφει JSON atomically (tmp + rename) με 0600."""
    try:
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=".config_", suffix=".tmp", dir=str(path.parent)
        )
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.chmod(tmp_path, 0o600)
            os.replace(tmp_path, path)
        except Exception:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
            raise
    except OSError as e:
        raise ConfigError(f"Αδυναμία εγγραφής config: {e}")


# ---------- Load / Save ----------

def _load_raw() -> Dict[str, Any]:
    """Διαβάζει το config από δίσκο. Αν λείπει/σπάσει → defaults."""
    if not CONFIG_FILE.exists():
        return _deep_copy_defaults()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Corrupted → κρατάμε backup και γυρνάμε defaults
        try:
            backup = CONFIG_FILE.with_suffix(".json.corrupted")
            os.replace(CONFIG_FILE, backup)
        except OSError:
            pass
        return _deep_copy_defaults()
    except OSError:
        return _deep_copy_defaults()

    if not isinstance(data, dict):
        return _deep_copy_defaults()

    return _merge_defaults(data)


def get_config() -> Dict[str, Any]:
    """Επιστρέφει το τρέχον config (πάντα έγκυρο, με defaults συμπληρωμένα)."""
    return _load_raw()


def save_config(cfg: Dict[str, Any]) -> None:
    """Αποθηκεύει το config atomically. Απαιτεί dict."""
    if not isinstance(cfg, dict):
        raise ConfigError("Το config πρέπει να είναι dict")
    _ensure_dir()
    _write_atomic(CONFIG_FILE, cfg)


# ---------- API Keys ----------

def get_api_key(provider: str) -> str:
    """Επιστρέφει το API key για τον provider (ή κενό string)."""
    cfg = _load_raw()
    providers = cfg.get("providers", {})
    if provider not in providers:
        return ""
    return providers[provider].get("api_key", "") or ""


def set_api_key(provider: str, key: str) -> None:
    """Ορίζει το API key για τον provider."""
    if not isinstance(key, str):
        raise ConfigError("Το API key πρέπει να είναι string")
    cfg = _load_raw()
    if provider not in cfg["providers"]:
        raise ConfigError(f"Άγνωστος provider: {provider}")
    cfg["providers"][provider]["api_key"] = key.strip()
    save_config(cfg)


def has_api_key(provider: str) -> bool:
    return bool(get_api_key(provider))


# ---------- Provider ----------

def get_active_provider() -> str:
    cfg = _load_raw()
    return cfg.get("active_provider", "openai")


def set_active_provider(provider: str) -> None:
    cfg = _load_raw()
    if provider not in cfg["providers"]:
        raise ConfigError(f"Άγνωστος provider: {provider}")
    cfg["active_provider"] = provider
    save_config(cfg)


def get_default_model(provider: str) -> str:
    cfg = _load_raw()
    providers = cfg.get("providers", {})
    if provider not in providers:
        return ""
    return providers[provider].get("default_model", "")


def set_default_model(provider: str, model: str) -> None:
    cfg = _load_raw()
    if provider not in cfg["providers"]:
        raise ConfigError(f"Άγνωστος provider: {provider}")
    cfg["providers"][provider]["default_model"] = model
    save_config(cfg)


# ---------- Onboarding ----------

def is_onboarding_completed() -> bool:
    return bool(_load_raw().get("onboarding_completed", False))


def mark_onboarding_completed() -> None:
    cfg = _load_raw()
    cfg["onboarding_completed"] = True
    save_config(cfg)


# ---------- Misc ----------

def get_language() -> str:
    return _load_raw().get("language", "el")


def set_language(lang: str) -> None:
    cfg = _load_raw()
    cfg["language"] = lang
    save_config(cfg)


def get_theme() -> str:
    return _load_raw().get("theme", "dark")


def set_theme(mode: str) -> None:
    cfg = _load_raw()
    cfg["theme"] = mode
    save_config(cfg)


def reset_config() -> None:
    """Σβήνει το config (για testing)."""
    if CONFIG_FILE.exists():
        try:
            os.unlink(CONFIG_FILE)
        except OSError as e:
            raise ConfigError(f"Αδυναμία διαγραφής config: {e}")


def config_path() -> Path:
    """Επιστρέφει το path του config file."""
    return CONFIG_FILE