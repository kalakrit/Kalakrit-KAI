# app.py (Updated UI only, original logic intact)
import customtkinter as ctk
from tkinter import messagebox, Toplevel
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import webbrowser
import threading
import tempfile
from playsound import playsound
from language_map import get_language_names, get_code_by_name, get_name_by_code, detect_language_code, is_voice_supported
import whisper
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("orange.json")

whisper_model = whisper.load_model("base")

class KalakritKAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("kalakrit KAI")
        self.geometry("1200x700")
        self.resizable(False, False)
        self.configure(fg_color="#FFF7F2")

        self.kai_variants = ["KAI", "काई", "ਕਾਈ", "కాయి", "கை", "ಕೈ", "കൈ", "كاي", "カイ", "凯"]
        self.kai_index = 0
        self.translator = Translator()

        self.create_widgets()
        self.rotate_kai_text()

    def create_widgets(self):
        self.logo_label = ctk.CTkLabel(self, text="kalakrit", font=("Segoe UI", 28, "bold"), text_color="#000000")
        self.logo_label.place(x=20, y=20)
        self.kai_label = ctk.CTkLabel(self, text="KAI", font=("Segoe UI", 28, "bold"), text_color="#000000")
        self.kai_label.place(x=150, y=20)

        self.menu_btn = ctk.CTkButton(self, text="☰", width=40, height=32, fg_color="#333333", hover_color="#555555",
                                      text_color="#FFFFFF", command=self.toggle_menu)
        self.menu_btn.place(x=1120, y=20)

        self.input_card = ctk.CTkFrame(self, width=500, height=150, corner_radius=25, fg_color="#FFFFFF")
        self.input_card.place(x=80, y=100)
        self.lang_title = ctk.CTkLabel(self.input_card, text="Detected Language", font=("Segoe UI", 16), text_color="#666666")
        self.lang_title.place(x=20, y=10)
        self.input_label = ctk.CTkLabel(self.input_card, text="", font=("Segoe UI", 22, "bold"), text_color="#000000")
        self.input_label.place(x=20, y=50)
        self.mic_btn = ctk.CTkButton(self.input_card, text="🎤", width=40, height=40, fg_color="#FF6D2F", command=self.start_listening)
        self.mic_btn.place(x=430, y=90)

        self.output_card = ctk.CTkFrame(self, width=500, height=150, corner_radius=25, fg_color="#FFFFFF")
        self.output_card.place(x=80, y=270)
        self.output_lang_label = ctk.CTkLabel(self.output_card, text="", font=("Segoe UI", 16), text_color="#666666")
        self.output_lang_label.place(x=20, y=10)
        self.translated_label = ctk.CTkLabel(self.output_card, text="", font=("Segoe UI", 22, "bold"), text_color="#5A2B13")
        self.translated_label.place(x=20, y=50)
        self.speaker_btn = ctk.CTkButton(self.output_card, text="🔊", width=40, height=40, fg_color="#333333", command=self.speak_output)
        self.speaker_btn.place(x=430, y=90)

        self.support_title = ctk.CTkLabel(self, text="Need Help? We're Here for You", font=("Segoe UI", 22, "bold"), text_color="#000000")
        self.support_title.place(relx=0.5, y=460, anchor="center")

        self.write_card = ctk.CTkFrame(self, width=280, height=140, corner_radius=20, fg_color="#FFFFFF")
        self.write_card.place(x=240, y=500)
        ctk.CTkLabel(self.write_card, text="Write to Us", font=("Segoe UI", 18, "bold"), text_color="#000000").place(x=20, y=10)
        ctk.CTkLabel(self.write_card, text="Reach us via email for\ntranslation help, app support,\nor collaboration queries.",
                     font=("Segoe UI", 13), text_color="#333333", justify="left").place(x=20, y=45)
        ctk.CTkButton(self.write_card, text="Write an Email", width=120, fg_color="#FF6D2F",
                      command=lambda: webbrowser.open("mailto:lokalisuno@kalakrit.in")).place(x=70, y=100)

        self.call_card = ctk.CTkFrame(self, width=280, height=140, corner_radius=20, fg_color="#FFFFFF")
        self.call_card.place(x=630, y=500)
        ctk.CTkLabel(self.call_card, text="Call Support Helpline", font=("Segoe UI", 18, "bold"), text_color="#000000").place(x=20, y=10)
        ctk.CTkLabel(self.call_card, text="Available 7 days a week for\nurgent support or inquiries.", font=("Segoe UI", 13),
                     text_color="#333333").place(x=20, y=50)
        ctk.CTkButton(self.call_card, text="Give us a call", width=120, fg_color="#FF6D2F",
                      command=lambda: messagebox.showinfo("Call", "Call us at 7042190859")).place(x=70, y=100)

        ctk.CTkLabel(self, text="kalakrit Studios", font=("Segoe UI", 18, "bold"), text_color="#000000").place(relx=0.5, y=670, anchor="center")

    def toggle_menu(self):
        if hasattr(self, "menu_frame") and self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None
        else:
            self.menu_frame = ctk.CTkFrame(self, width=260, height=370, corner_radius=12, fg_color="#333333")
            self.menu_frame.place(x=910, y=60)

            ctk.CTkButton(self.menu_frame, text="About Us", fg_color="#444444", text_color="#FFFFFF", command=lambda: self.open_info_window(
                "About Us",
                "Kalakrit KAI (Kalakrit Artificial Insaan) is an advanced multilingual voice translator developed by Kalakrit Studios.\n\nWe specialize in:\n• Voice-over and dubbing\n• AI-powered real-time translation\n• Multilingual education tools\n• Real-time interpretation"
            )).pack(pady=4)

            ctk.CTkButton(self.menu_frame, text="Partner with Kalakrit", fg_color="#444444", text_color="#FFFFFF", command=lambda: self.open_info_window(
                "Partner with Kalakrit",
                "Kalakrit Studios invites partnerships with:\n• EdTech startups\n• Media companies\n• Educational institutions\n• Global brands\n\nWe provide:\n• AI voice tools\n• Custom translation solutions\n• White-label integrations"
            )).pack(pady=4)

            ctk.CTkButton(self.menu_frame, text="Services We Provide", fg_color="#444444", text_color="#FFFFFF", command=lambda: self.open_info_window(
                "Services We Provide",
                "✔ Real-time multilingual voice translation\n✔ Dubbing & voice-over for videos\n✔ Localization of training content\n✔ Event interpretation tools\n✔ Custom AI chatbot solutions"
            )).pack(pady=4)

            social_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
            social_frame.pack(pady=8)

            links = [
                ("Instagram.png", "https://www.instagram.com/kalakrit.in"),
                ("Facebook.png", "https://www.facebook.com/Kalakritofficial/"),
                ("Youtube.png", "https://www.youtube.com/@Kalakrit"),
                ("Linkedin.png", "https://www.linkedin.com/company/kalakrit")
            ]
            for icon_path, link in links:
                try:
                    img = ctk.CTkImage(light_image=Image.open(icon_path), size=(24, 24))
                    btn = ctk.CTkButton(social_frame, text="", width=36, height=36, image=img,
                                        fg_color="#555555", command=lambda l=link: webbrowser.open(l))
                    btn.pack(side="left", padx=4)
                except Exception as e:
                    print(f"Error loading icon: {icon_path} — {e}")

    def rotate_kai_text(self):
        self.kai_label.configure(text=self.kai_variants[self.kai_index])
        self.kai_index = (self.kai_index + 1) % len(self.kai_variants)
        self.after(3000, self.rotate_kai_text)

    def start_listening(self):
        threading.Thread(target=self.process_speech).start()

    def process_speech(self):
        try:
            self.input_label.configure(text="Speak now...")
            self.update()

            audio_path = os.path.join(tempfile.gettempdir(), "input.wav")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                with open(audio_path, "wb") as f:
                    f.write(audio.get_wav_data())

            result = whisper_model.transcribe(audio_path)
            user_text = result["text"]
            from_lang_code = detect_language_code(user_text)
            from_lang_name = get_name_by_code(from_lang_code) or from_lang_code.upper()

            self.input_label.configure(text=user_text)
            self.lang_title.configure(text=f"Detected Language: {from_lang_name}")

            self.speak_text("Please say the language you want translation in.", from_lang_code)
            self.update()

            with sr.Microphone() as source:
                lang_audio = r.listen(source)
                with open("lang_input.wav", "wb") as f:
                    f.write(lang_audio.get_wav_data())
            result_lang = whisper_model.transcribe("lang_input.wav")
            lang_name = result_lang["text"].strip()
            lang_code = get_code_by_name(lang_name)

            if not lang_code:
                self.output_lang_label.configure(text="Unsupported Language")
                self.translated_label.configure(text="Could not detect language")
                self.speak_text("Sorry, I could not detect the target language.", from_lang_code)
                return

            self.output_lang_label.configure(text=lang_name)
            translated = self.translator.translate(user_text, dest=lang_code).text
            self.translated_label.configure(text=translated)

            if is_voice_supported(lang_name):
                self.speak_text(translated, lang_code)

        except Exception as e:
            self.input_label.configure(text="Error")
            messagebox.showerror("Error", str(e))

    def speak_text(self, text, lang_code='hi'):
        try:
            temp_path = os.path.join(tempfile.gettempdir(), "kalakrit_temp.mp3")
            tts = gTTS(text=text, lang=lang_code)
            tts.save(temp_path)
            playsound(temp_path)
            os.remove(temp_path)
        except Exception as e:
            messagebox.showerror("TTS Error", str(e))

    def speak_output(self):
        text = self.translated_label.cget("text")
        lang_name = self.output_lang_label.cget("text")
        lang_code = get_code_by_name(lang_name)
        if text and lang_code:
            self.speak_text(text, lang_code)

    def open_info_window(self, title, message):
        popup = Toplevel(self)
        popup.title(title)
        popup.geometry("800x500")
        popup.configure(bg="#FF6D2F")
        label_frame = ctk.CTkFrame(popup, fg_color="#FF6D2F", width=480, height=400)
        label_frame.place(x=20, y=20)
        label = ctk.CTkLabel(label_frame, text=message, text_color="#000000", fg_color="#FF6D2F",
                             font=("Segoe UI", 20, "bold"), wraplength=560, justify="left", anchor="nw")
        label.pack(padx=5, pady=5, anchor="w")

if __name__ == "__main__":
    app = KalakritKAI()
    app.mainloop()
