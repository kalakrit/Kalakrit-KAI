import pyttsx3
from language_map import get_code_by_name, is_voice_supported
from gtts import gTTS
from playsound import playsound
import tempfile
import os

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Set English voice (gender not required anymore)
def set_english_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if "en" in voice.id.lower():
            engine.setProperty('voice', voice.id)
            return
    engine.setProperty('voice', voices[0].id)  # fallback

# Speak using pyttsx3

def speak_with_pyttsx3(text):
    try:
        set_english_voice()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"🔴 pyttsx3 Error: {e}")

# Speak using gTTS

def speak_with_gtts(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            path = tmp.name
            tts.save(path)
        playsound(path)
        os.remove(path)
    except Exception as e:
        print(f"🔴 gTTS Error: {e}")

# Master function

def speak_text(text, lang_name):
    lang_code = get_code_by_name(lang_name)
    if not lang_code:
        print(f"❗ Language not found: {lang_name}")
        return

    print(f"🗣 Speaking in {lang_name} ({lang_code})")

    if lang_code == "en":
        speak_with_pyttsx3(text)
    elif is_voice_supported(lang_name):
        speak_with_gtts(text, lang_code)
    else:
        print(f"🔇 Voice not supported for {lang_name}")
