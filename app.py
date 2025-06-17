# streamlit_app.py
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import tempfile
from playsound import playsound
from language_map import get_language_names, get_code_by_name, get_name_by_code, detect_language_code, is_voice_supported
import whisper
from PIL import Image

# Load whisper model
whisper_model = whisper.load_model("base")
translator = Translator()

# App title
st.set_page_config(page_title="kalakrit KAI", layout="wide")
st.markdown("<h1 style='color:black; font-size: 40px;'>kalakrit <span style='color:#FF6D2F'>KAI</span></h1>", unsafe_allow_html=True)

# Sidebar Menu
with st.sidebar:
    st.header("☰ Menu")
    with st.expander("About Us"):
        st.markdown("""
        Kalakrit KAI (Kalakrit Artificial Insaan) is an advanced multilingual voice translator developed by Kalakrit Studios.
        
        We specialize in:
        - Voice-over and dubbing  
        - AI-powered real-time translation  
        - Multilingual education tools  
        - Real-time interpretation  
        
        **Our mission:** Break language barriers using voice-based AI tools for students, creators, and businesses.
        """)
    
    with st.expander("Partner with Kalakrit"):
        st.markdown("""
        Kalakrit Studios invites partnerships with:  
        - EdTech startups  
        - Media companies  
        - Educational institutions  
        - Global brands  
        
        We provide:
        - AI voice tools  
        - Custom translation solutions  
        - White-label integrations  
        
        📩 Contact us via business email or Google Form.
        """)

    with st.expander("Services We Provide"):
        st.markdown("""
        - Real-time multilingual voice translation  
        - Dubbing & voice-over for videos  
        - Localization of training content  
        - Event interpretation tools  
        - Custom AI chatbot solutions  
        """)

    st.markdown("#### 🌐 Social Media")
    cols = st.columns(4)
    links = [
        ("Instagram.png", "https://www.instagram.com/kalakrit.in"),
        ("Facebook.png", "https://www.facebook.com/Kalakritofficial/"),
        ("Youtube.png", "https://www.youtube.com/@Kalakrit"),
        ("Linkedin.png", "https://www.linkedin.com/company/kalakrit")
    ]
    for i, (icon, url) in enumerate(links):
        with cols[i]:
            if os.path.exists(icon):
                st.image(icon, width=30)
                st.markdown(f"[Click here]({url})", unsafe_allow_html=True)
            else:
                st.warning(f"Missing {icon}")

# Input section
st.markdown("---")
st.subheader("🎤 Voice Input")
if st.button("Start Speaking"):
    try:
        with st.spinner("Listening..."):
            temp_audio_path = os.path.join(tempfile.gettempdir(), "input.wav")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                with open(temp_audio_path, "wb") as f:
                    f.write(audio.get_wav_data())

            result = whisper_model.transcribe(temp_audio_path)
            user_text = result["text"]
            from_lang_code = detect_language_code(user_text)
            from_lang_name = get_name_by_code(from_lang_code) or from_lang_code.upper()

            st.success(f"Input Detected: {user_text}")
            st.info(f"Detected Language: {from_lang_name}")

            tts_prompt = "Please say the language you want translation in."
            tts = gTTS(text=tts_prompt, lang=from_lang_code)
            temp_path = os.path.join(tempfile.gettempdir(), "prompt.mp3")
            tts.save(temp_path)
            playsound(temp_path)
            os.remove(temp_path)

            with sr.Microphone() as source:
                lang_audio = r.listen(source)
                with open("lang_input.wav", "wb") as f:
                    f.write(lang_audio.get_wav_data())

            result_lang = whisper_model.transcribe("lang_input.wav")
            lang_name = result_lang["text"].strip()
            lang_code = get_code_by_name(lang_name)

            if not lang_code:
                st.error("Unsupported or undetected target language.")
            else:
                st.success(f"Target Language: {lang_name}")
                translated = translator.translate(user_text, dest=lang_code).text
                st.markdown(f"### 📝 Translated Text: {translated}")

                if is_voice_supported(lang_name):
                    tts = gTTS(text=translated, lang=lang_code)
                    tts_path = os.path.join(tempfile.gettempdir(), "output.mp3")
                    tts.save(tts_path)
                    playsound(tts_path)
                    os.remove(tts_path)

    except Exception as e:
        st.error(f"Error: {e}")

# Support section
st.markdown("---")
st.markdown("### 🆘 Need Help? We're Here for You")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📧 Write to Us")
    st.write("Reach us via email for help, support, or collaboration.")
    if st.button("Write an Email"):
        st.markdown("[Click to Email](mailto:lokalisuno@kalakrit.in)")

with col2:
    st.subheader("📞 Call Support Helpline")
    st.write("Available 7 days a week for urgent inquiries.")
    if st.button("Give us a Call"):
        st.info("Call us at 7042190859")

st.markdown("### 🌍 kalakrit Studios")
