"""hello_world plugin — smoke test του plugin system.

2 tools:
- greet: χαιρετάει τον χρήστη
- echo: επαναλαμβάνει ένα μήνυμα

ΔΕΝ χρησιμοποιεί LLM. Όλα τοπικά.
"""

from core.plugin_base import BasePlugin
from core.types import ToolResult


GREETINGS = {
    "el": "Γεια σου, {name}! 👋",
    "en": "Hello, {name}! 👋",
}

FALLBACK_GREETING = "Γεια σου, {name}! 👋"


class Plugin(BasePlugin):
    """Πρώτο plugin — δείχνει ότι το system δουλεύει."""

    def run_tool(self, tool_name: str, params: dict) -> ToolResult:
        if tool_name == "greet":
            return self._greet(params)
        if tool_name == "echo":
            return self._echo(params)
        return ToolResult.fail(error=f"Άγνωστο tool: {tool_name}")

    def _greet(self, params: dict) -> ToolResult:
        name = params.get("name", "").strip()
        if not name:
            return ToolResult.fail(error="Το όνομα είναι υποχρεωτικό")

        lang = params.get("language", "el")
        template = GREETINGS.get(lang, FALLBACK_GREETING)
        greeting = template.format(name=name)

        return ToolResult.ok(
            data=greeting,
            lang=lang,
            name=name,
        )

    def _echo(self, params: dict) -> ToolResult:
        message = params.get("message", "")
        if not message:
            return ToolResult.fail(error="Το μήνυμα είναι υποχρεωτικό")

        try:
            times = int(params.get("times", 1))
        except (ValueError, TypeError):
            times = 1

        if times < 1:
            times = 1
        if times > 100:
            times = 100

        result = "\n".join([message] * times)

        return ToolResult.ok(
            data=result,
            times=times,
            length=len(message),
        )
