import streamlit as st


DEFAULT_LANG = "el"
SUPPORTED_LANGS = ["el", "en"]
LANG_LABELS = {"el": "🇬🇷 Ελληνικά", "en": "🇬🇧 English"}


TRANSLATIONS = {
    "el": {
        "app.title": "does4u Dashboard",
        "app.tagline": "Data • AI • Automation",
        "app.phase": "Phase 1.2 • i18n",

        "sidebar.brand": "🎯 does4u",
        "sidebar.theme_dark": "🌙 Dark mode",
        "sidebar.language": "🌐 Γλώσσα",

        "welcome.title": "Καλώς ήρθες, Μήτσο 👋",
        "welcome.subtitle": "Δείγμα του theme • Phase 1.2",

        "metric.progress": "Πρόοδος",
        "metric.progress_delta": "+1 σήμερα",
        "metric.plugins": "Plugins",
        "metric.plugins_delta": "σε ανάπτυξη",
        "metric.theme": "Theme",
        "metric.theme_delta": "✓",

        "button.primary": "Primary",
        "button.accent": "Accent",
        "button.cancel": "Άκυρο",

        "card.title": "🎨 Premium Card",
        "card.body": "Έτσι θα φαίνονται τα cards — με απαλές σκιές, στρογγυλεμένες γωνίες και consistent spacing.",

        "alert.success": "✅ Επιτυχία — αυτό είναι ένα success message",
        "alert.warning": "⚠️ Προσοχή — αυτό είναι ένα warning",
        "alert.error": "❌ Σφάλμα — αυτό είναι ένα error",

        "input.name": "Όνομα",
        "input.name_placeholder": "π.χ. Μήτσος",
        "input.amount": "Ποσό (€)",
        "input.notes": "Σημειώσεις",
        "input.notes_placeholder": "Γράψε κάτι...",
        "input.select": "Επιλογή",
        "input.select_option": "Επιλογή",

        "plugin.no_selection": "Δεν έχει επιλεγεί plugin",
        "plugin.no_selection_hint": "Διάλεξε ένα plugin από το μενού αριστερά.",
        "plugin.by": "από",
        "plugin.tools": "Εργαλεία",
        "plugin.no_tools": "Το plugin δεν έχει εργαλεία",
        "plugin.execute": "Εκτέλεση",
        "plugin.executing": "Εκτέλεση...",
        "plugin.result": "Αποτέλεσμα",
        "plugin.error": "Σφάλμα",
        "plugin.success": "Επιτυχία",
        "plugin.reset": "Καθαρισμός",
        "plugin.required": "υποχρεωτικό",
        "plugin.optional": "προαιρετικό",

        "onboarding.welcome": "Καλώς ήρθες στο does4u",
        "onboarding.subtitle": "Ας στήσουμε το dashboard σου σε 30 δευτερόλεπτα.",
        "onboarding.step_provider": "1. Διάλεξε LLM Provider",
        "onboarding.step_provider_hint": "Ποιον provider θα χρησιμοποιείς; Μπορείς να το αλλάξεις μετά.",
        "onboarding.step_key": "2. Βάλε το API Key σου",
        "onboarding.step_key_hint": "Το key αποθηκεύεται τοπικά στο PC σου. Δεν ανεβαίνει πουθενά.",
        "onboarding.privacy_warning": "⚠️ Το key αποθηκεύεται σε plaintext στο ~/.does4u/config.json. Χρησιμοποίησε ξεχωριστό key με spending limit.",
        "onboarding.step_prefs": "3. Προτιμήσεις",
        "onboarding.finish": "Ολοκλήρωση",
        "onboarding.skip": "Παράλειψη για τώρα",
        "onboarding.skip_hint": "Θα μπορείς να προσθέσεις API key αργότερα.",
        "onboarding.key_required": "Βάλε API key ή πάτα «Παράλειψη για τώρα».",
        "onboarding.provider_label": "Provider",
        "onboarding.key_label": "API Key",
        "onboarding.key_placeholder": "sk-...",
        "onboarding.lang_label": "Γλώσσα",
        "onboarding.theme_label": "Θέμα",
        "onboarding.theme_dark": "Σκούρο",
        "onboarding.theme_light": "Φωτεινό",
        "onboarding.footer": "does4u • Data • AI • Automation",

        "settings.title": "Ρυθμίσεις",
        "settings.subtitle": "Άλλαξε provider, API key ή προτιμήσεις.",
        "settings.save": "Αποθήκευση",
        "settings.saved": "✅ Αποθηκεύτηκε",
    },
    "en": {
        "app.title": "does4u Dashboard",
        "app.tagline": "Data • AI • Automation",
        "app.phase": "Phase 1.2 • i18n",

        "sidebar.brand": "🎯 does4u",
        "sidebar.theme_dark": "🌙 Dark mode",
        "sidebar.language": "🌐 Language",

        "welcome.title": "Welcome, Mitsos 👋",
        "welcome.subtitle": "Theme preview • Phase 1.2",

        "metric.progress": "Progress",
        "metric.progress_delta": "+1 today",
        "metric.plugins": "Plugins",
        "metric.plugins_delta": "in development",
        "metric.theme": "Theme",
        "metric.theme_delta": "✓",

        "button.primary": "Primary",
        "button.accent": "Accent",
        "button.cancel": "Cancel",

        "card.title": "🎨 Premium Card",
        "card.body": "This is how cards will look — with soft shadows, rounded corners, and consistent spacing.",

        "alert.success": "✅ Success — this is a success message",
        "alert.warning": "⚠️ Warning — this is a warning",
        "alert.error": "❌ Error — this is an error",

        "input.name": "Name",
        "input.name_placeholder": "e.g. Mitsos",
        "input.amount": "Amount (€)",
        "input.notes": "Notes",
        "input.notes_placeholder": "Type something...",
        "input.select": "Select",
        "input.select_option": "Option",

        "plugin.no_selection": "No plugin selected",
        "plugin.no_selection_hint": "Pick a plugin from the menu on the left.",
        "plugin.by": "by",
        "plugin.tools": "Tools",
        "plugin.no_tools": "This plugin has no tools",
        "plugin.execute": "Execute",
        "plugin.executing": "Executing...",
        "plugin.result": "Result",
        "plugin.error": "Error",
        "plugin.success": "Success",
        "plugin.reset": "Clear",
        "plugin.required": "required",
        "plugin.optional": "optional",

        "onboarding.welcome": "Welcome to does4u",
        "onboarding.subtitle": "Let's set up your dashboard in 30 seconds.",
        "onboarding.step_provider": "1. Choose LLM Provider",
        "onboarding.step_provider_hint": "Which provider will you use? You can change it later.",
        "onboarding.step_key": "2. Enter your API Key",
        "onboarding.step_key_hint": "The key is stored locally on your PC. It is never uploaded anywhere.",
        "onboarding.privacy_warning": "⚠️ Key is stored in plaintext at ~/.does4u/config.json. Use a dedicated key with a spending limit.",
        "onboarding.step_prefs": "3. Preferences",
        "onboarding.finish": "Finish",
        "onboarding.skip": "Skip for now",
        "onboarding.skip_hint": "You can add an API key later.",
        "onboarding.key_required": "Enter API key or click «Skip for now».",
        "onboarding.provider_label": "Provider",
        "onboarding.key_label": "API Key",
        "onboarding.key_placeholder": "sk-...",
        "onboarding.lang_label": "Language",
        "onboarding.theme_label": "Theme",
        "onboarding.theme_dark": "Dark",
        "onboarding.theme_light": "Light",
        "onboarding.footer": "does4u • Data • AI • Automation",

        "settings.title": "Settings",
        "settings.subtitle": "Change provider, API key, or preferences.",
        "settings.save": "Save",
        "settings.saved": "✅ Saved",
    },
}


def get_lang():
    if "lang" not in st.session_state:
        st.session_state.lang = DEFAULT_LANG
    return st.session_state.lang


def set_lang(lang):
    if lang in SUPPORTED_LANGS:
        st.session_state.lang = lang


def t(key, lang=None):
    if lang is None:
        lang = get_lang()
    if lang not in TRANSLATIONS:
        lang = DEFAULT_LANG
    return TRANSLATIONS[lang].get(key, f"[{key}]")


def all_langs():
    return SUPPORTED_LANGS


def lang_label(code):
    return LANG_LABELS.get(code, code)