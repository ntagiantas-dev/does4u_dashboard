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