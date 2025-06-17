from googletrans import Translator

translator = Translator()

def translate_text(text, src_lang_code, dest_lang_code):
    """
    Translates the given text from source language to destination language.
    """
    try:
        result = translator.translate(text, src=src_lang_code, dest=dest_lang_code)
        print(f"🔁 Translation: [{src_lang_code}] → [{dest_lang_code}] = {result.text}")
        return result.text
    except Exception as e:
        print(f"[Translation Error] {str(e)}")
        return "[Translation Failed]"

def detect_language_code(text):
    """
    Detects the language code (e.g., 'en', 'hi') of the provided text.
    """
    try:
        detected = translator.detect(text)
        print(f"🔍 Detected Language: {detected.lang} with confidence {detected.confidence}")
        return detected.lang
    except Exception as e:
        print(f"[Detection Error] {str(e)}")
        return None
