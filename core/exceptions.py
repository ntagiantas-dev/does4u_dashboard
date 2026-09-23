"""Exceptions για το plugin system του does4u Dashboard."""


class Does4uError(Exception):
    """Base exception για όλα τα does4u errors."""
    pass


class PluginError(Does4uError):
    """Γενικό σφάλμα plugin."""
    pass


class ManifestError(PluginError):
    """Σφάλμα στο plugin manifest (YAML)."""
    pass


class PluginLoadError(PluginError):
    """Σφάλμα κατά τη φόρτωση plugin."""
    pass


class ToolNotFoundError(PluginError):
    """Το ζητούμενο tool δεν υπάρχει στο plugin."""
    pass


class ToolExecutionError(PluginError):
    """Σφάλμα κατά την εκτέλεση tool."""
    pass


class ConfigError(Does4uError):
    """Σφάλμα στο config (BYOK, keys)."""
    pass
