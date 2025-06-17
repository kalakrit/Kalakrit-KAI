import os
from gtts import gTTS
from playsound import playsound
from language_map import get_code_by_name, is_voice_supported
import tempfile

# Directory to store temporary voice files
VOICE_FOLDER = "voices"
os.makedirs(VOICE_FOLDER, exist_ok=True)

def speak_text(text, lang_name):
    lang_code = get_code_by_name(lang_name)

    if not lang_code:
        print(f"[TTS] ❌ Language code not found for: {lang_name}")
        return

    if not is_voice_supported(lang_name):
        print(f"[TTS] ⚠ Voice not supported for {lang_name}")
        return

    try:
        print(f"[TTS] 🎙 Speaking in {lang_name} ({lang_code})")
        tts = gTTS(text=text, lang=lang_code, slow=False)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=VOICE_FOLDER) as temp_file:
            temp_path = temp_file.name
            tts.save(temp_path)

        playsound(temp_path)
        os.remove(temp_path)

    except Exception as e:
        print(f"[TTS ERROR] ❌ {str(e)}")
