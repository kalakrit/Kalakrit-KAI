import speech_recognition as sr
import whisper
import tempfile
import os
import torch

#ffmpeg.exe path
os.environ["PATH"] += os.pathsep + r"C:\Users\Arpita Gangwani\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin"


# Use tiny or base for faster response (optional: tiny.en, base, small)
model = whisper.load_model("base")

recognizer = sr.Recognizer()

def recognize_speech_from_mic(timeout=6):
    try:
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout)

        # Save audio to temp file for whisper
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav_path = f.name
            with open(wav_path, "wb") as audio_file:
                audio_file.write(audio.get_wav_data())

        print("🧠 Processing with Whisper...")
        result = model.transcribe(wav_path, fp16=torch.cuda.is_available())
        os.remove(wav_path)

        text = result.get("text", "").strip()
        if text:
            print(f"✅ Recognized: {text}")
            return text
        else:
            print("❌ Whisper found no speech.")
            return None

    except sr.WaitTimeoutError:
        print("⌛ Timeout: No speech.")
        return None
    except sr.UnknownValueError:
        print("❌ Could not understand.")
        return None
    except sr.RequestError as e:
        print(f"⚠ API error: {e}")
        return None
    except Exception as e:
        print(f"⚠ Whisper fallback failed: {e}")
        return None
