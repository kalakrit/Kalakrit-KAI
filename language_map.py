# Kalakrit KAI Language Support Map

LANGUAGES = [
    # 🇮🇳 Indian Languages
    {"name": "Assamese", "code": "as", "voice_supported": False},
    {"name": "Bengali", "code": "bn", "voice_supported": True},
    {"name": "Gujarati", "code": "gu", "voice_supported": True},
    {"name": "Hindi", "code": "hi", "voice_supported": True},
    {"name": "Kannada", "code": "kn", "voice_supported": True},
    {"name": "Konkani", "code": "kok", "voice_supported": False},
    {"name": "Malayalam", "code": "ml", "voice_supported": True},
    {"name": "Manipuri", "code": "mni", "voice_supported": False},
    {"name": "Marathi", "code": "mr", "voice_supported": True},
    {"name": "Punjabi", "code": "pa", "voice_supported": True},
    {"name": "Sindhi", "code": "sd", "voice_supported": False},
    {"name": "Tamil", "code": "ta", "voice_supported": True},
    {"name": "Telugu", "code": "te", "voice_supported": True},
    {"name": "Urdu", "code": "ur", "voice_supported": True},

    # 🌍 Global (Non-Indian) Languages
    {"name": "Afrikaans", "code": "af", "voice_supported": True},
    {"name": "Arabic", "code": "ar", "voice_supported": True},
    {"name": "Bulgarian", "code": "bg", "voice_supported": True},
    {"name": "Catalan", "code": "ca", "voice_supported": True},
    {"name": "Chinese (Mandarin)", "code": "zh-cn", "voice_supported": True},
    {"name": "Croatian", "code": "hr", "voice_supported": True},
    {"name": "Czech", "code": "cs", "voice_supported": True},
    {"name": "Danish", "code": "da", "voice_supported": True},
    {"name": "Dutch", "code": "nl", "voice_supported": True},
    {"name": "English", "code": "en", "voice_supported": True},
    {"name": "Filipino", "code": "tl", "voice_supported": True},
    {"name": "Finnish", "code": "fi", "voice_supported": True},
    {"name": "French", "code": "fr", "voice_supported": True},
    {"name": "German", "code": "de", "voice_supported": True},
    {"name": "Greek", "code": "el", "voice_supported": True},
    # {"name": "Hebrew", "code": "he", "voice_supported": True},
    {"name": "Hungarian", "code": "hu", "voice_supported": True},
    {"name": "Indonesian", "code": "id", "voice_supported": True},
    {"name": "Italian", "code": "it", "voice_supported": True},
    {"name": "Japanese", "code": "ja", "voice_supported": True},
    {"name": "Korean", "code": "ko", "voice_supported": True},
    {"name": "Latvian", "code": "lv", "voice_supported": True},
    {"name": "Lithuanian", "code": "lt", "voice_supported": True},
    {"name": "Malay", "code": "ms", "voice_supported": True},
    {"name": "Nepali", "code": "ne", "voice_supported": True},
    {"name": "Norwegian", "code": "no", "voice_supported": True},
    # {"name": "Persian", "code": "fa", "voice_supported": True},
    {"name": "Polish", "code": "pl", "voice_supported": True},
    {"name": "Portuguese", "code": "pt", "voice_supported": True},
    {"name": "Romanian", "code": "ro", "voice_supported": True},
    {"name": "Russian", "code": "ru", "voice_supported": True},
    {"name": "Slovak", "code": "sk", "voice_supported": True},
    {"name": "Spanish", "code": "es", "voice_supported": True},
    {"name": "Swahili", "code": "sw", "voice_supported": True},
    {"name": "Swedish", "code": "sv", "voice_supported": True},
    {"name": "Thai", "code": "th", "voice_supported": True},
    {"name": "Turkish", "code": "tr", "voice_supported": True},
    {"name": "Ukrainian", "code": "uk", "voice_supported": True},
    {"name": "Vietnamese", "code": "vi", "voice_supported": True},
    # {"name": "Zulu", "code": "zu", "voice_supported": True}
]

def get_language_names():
    return sorted([lang["name"] for lang in LANGUAGES])

def get_name_by_code(code):
    code = code.strip().lower()
    for lang in LANGUAGES:
        if lang["code"].lower() == code:
            return lang["name"]
    return None

def get_code_by_name(name):
    name = name.strip().lower()
    for lang in LANGUAGES:
        if lang["name"].lower() == name:
            return lang["code"]
    return None

def is_voice_supported(name):
    name = name.strip().lower()
    for lang in LANGUAGES:
        if lang["name"].lower() == name:
            return lang["voice_supported"]
    return False

# 🔍 Language Detection (via Google Translate)
from googletrans import Translator

def detect_language_code(text):
    """
    Detects the language code (like 'hi', 'en', etc.) for a given text using Google Translate API.
    """
    translator = Translator()
    try:
        detection = translator.detect(text)
        return detection.lang
    except Exception as e:
        print("Error detecting language:", e)
        return "en"  # fallback to English if detection fails
