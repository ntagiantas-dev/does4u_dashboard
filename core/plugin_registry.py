"""Plugin Registry: auto-discovery + dynamic loading.

Σκανάρει έναν φάκελο με plugins, φορτώνει κάθε ένα,
και κρατάει instances σε map (name → BasePlugin).

Design:
- Robust: ένα σπασμένο plugin δεν ρίχνει τα άλλα
- Lazy-friendly: μπορεί να φορτώσει όλα ή ένα-ένα
- MCP-ready: εκθέτει list_tools() για ntad/MCP host
"""

import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.exceptions import PluginLoadError, PluginError
from core.manifest import parse_manifest_file
from core.plugin_base import BasePlugin


MANIFEST_FILENAME = "plugin.yaml"
PLUGIN_FILENAME = "plugin.py"
PLUGIN_CLASS_NAME = "Plugin"


class PluginRegistry:
    """Registry που ανακαλύπτει και φορτώνει plugins από έναν φάκελο."""

    def __init__(self, plugins_dir: Path):
        self.plugins_dir = Path(plugins_dir)
        self._plugins: Dict[str, BasePlugin] = {}
        self._errors: Dict[str, str] = {}

    # ---------- Discovery ----------

    def discover(self) -> List[Path]:
        """Βρίσκει όλους τους υποφακέλους που έχουν plugin.yaml + plugin.py."""
        if not self.plugins_dir.exists():
            return []

        candidates: List[Path] = []
        for child in sorted(self.plugins_dir.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith((".", "_")):
                continue
            if (child / MANIFEST_FILENAME).is_file() and (child / PLUGIN_FILENAME).is_file():
                candidates.append(child)
        return candidates

    # ---------- Loading ----------

    def load_one(self, plugin_dir: Path) -> BasePlugin:
        """Φορτώνει ένα plugin από τον φάκελό του.

        Raises:
            PluginLoadError: αν κάτι πάει λάθος.
        """
        plugin_dir = Path(plugin_dir)
        manifest_path = plugin_dir / MANIFEST_FILENAME
        plugin_file = plugin_dir / PLUGIN_FILENAME

        # 1. Parse manifest
        try:
            manifest = parse_manifest_file(manifest_path)
        except PluginError as e:
            raise PluginLoadError(f"Manifest error: {e}") from e

        # 2. Import plugin.py δυναμικά
        module_name = f"does4u_plugins.{plugin_dir.name}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"Αδυναμία φόρτωσης module: {plugin_file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            del sys.modules[module_name]
            raise PluginLoadError(
                f"Σφάλμα εκτέλεσης {plugin_file.name}: {e}"
            ) from e

        # 3. Βρες την κλάση Plugin
        if not hasattr(module, PLUGIN_CLASS_NAME):
            raise PluginLoadError(
                f"Το {plugin_file.name} δεν ορίζει κλάση '{PLUGIN_CLASS_NAME}'"
            )

        plugin_class = getattr(module, PLUGIN_CLASS_NAME)

        if not isinstance(plugin_class, type) or not issubclass(plugin_class, BasePlugin):
            raise PluginLoadError(
                f"Το '{PLUGIN_CLASS_NAME}' στο {plugin_file.name} δεν κληρονομεί από BasePlugin"
            )

        # 4. Instantiate + attach manifest
        try:
            instance = plugin_class()
        except Exception as e:
            raise PluginLoadError(f"Σφάλμα instantiate: {e}") from e

        instance.attach_manifest(manifest)

        # 5. Sanity check: manifest name != κενό
        if not instance.manifest.name:
            raise PluginLoadError("Το manifest έχει κενό name")

        return instance

    # ---------- Public API ----------

    def load_all(self) -> Dict[str, Any]:
        """Φορτώνει όλα τα plugins. Επιστρέφει summary.

        ΔΕΝ πετάει exception αν ένα plugin αποτύχει — το καταγράφει
        στο self._errors και συνεχίζει.
        """
        self._plugins.clear()
        self._errors.clear()

        candidates = self.discover()

        for plugin_dir in candidates:
            try:
                instance = self.load_one(plugin_dir)
            except PluginLoadError as e:
                self._errors[plugin_dir.name] = str(e)
                continue
            except Exception as e:
                self._errors[plugin_dir.name] = (
                    f"Απρόσμενο σφάλμα: {e}\n{traceback.format_exc()}"
                )
                continue

            name = instance.manifest.name

            if name in self._plugins:
                self._errors[plugin_dir.name] = (
                    f"Διπλότυπο name '{name}' — υπάρχει ήδη"
                )
                continue

            self._plugins[name] = instance

        return {
            "loaded": list(self._plugins.keys()),
            "failed": dict(self._errors),
            "total_discovered": len(candidates),
            "total_loaded": len(self._plugins),
            "total_failed": len(self._errors),
        }

    def get(self, name: str) -> Optional[BasePlugin]:
        """Επιστρέφει plugin by name ή None."""
        return self._plugins.get(name)

    def get_or_raise(self, name: str) -> BasePlugin:
        """Όπως το get(), αλλά πετάει PluginError αν λείπει."""
        p = self._plugins.get(name)
        if p is None:
            raise PluginError(f"Το plugin '{name}' δεν είναι φορτωμένο")
        return p

    def all(self) -> List[BasePlugin]:
        """Όλα τα φορτωμένα plugins."""
        return list(self._plugins.values())

    def names(self) -> List[str]:
        """Ονόματα όλων των φορτωμένων plugins."""
        return sorted(self._plugins.keys())

    def count(self) -> int:
        return len(self._plugins)

    def has(self, name: str) -> bool:
        return name in self._plugins

    def get_errors(self) -> Dict[str, str]:
        """Λάθη από το τελευταίο load_all()."""
        return dict(self._errors)

    # ---------- MCP-ready ----------

    def list_all_tools(self) -> List[Dict[str, Any]]:
        """Όλα τα tools όλων των plugins σε MCP format.

        Αυτό θα καλέσει ο ntad ή ένας MCP host για να δει
        τι tools υπάρχουν διαθέσιμα.
        """
        tools: List[Dict[str, Any]] = []
        for plugin in self._plugins.values():
            for tool_schema in plugin.to_mcp_tools():
                tools.append({
                    "plugin": plugin.manifest.name,
                    "tool": tool_schema,
                })
        return tools

    def execute(self, plugin_name: str, tool_name: str, params: Optional[Dict[str, Any]] = None):
        """Εκτελεί ένα tool από ένα plugin.

        Public API για ntad / UI / MCP host.
        """
        plugin = self.get_or_raise(plugin_name)
        return plugin.execute(tool_name, params or {})

    # ---------- Debug ----------

    def summary(self) -> str:
        """Human-readable σύνοψη για debugging."""
        lines = [
            f"PluginRegistry: {self.plugins_dir}",
            f"  Discovered: {len(self.discover())}",
            f"  Loaded:     {self.count()}",
            f"  Failed:     {len(self._errors)}",
        ]
        if self._plugins:
            lines.append("  Plugins:")
            for name, p in self._plugins.items():
                lines.append(f"    - {name} v{p.manifest.version} ({len(p.list_tools())} tools)")
        if self._errors:
            lines.append("  Errors:")
            for name, err in self._errors.items():
                lines.append(f"    - {name}: {err}")
        return "\n".join(lines)