import speech_recognition as sr
import wave
import os
from datetime import datetime

class RealTimeRecorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.setup_microphone()
    
    def setup_microphone(self):
        """Setup microphone with ambient noise adjustment"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone setup completed")
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
    
    def record_audio(self, duration=5, filename=None):
        """Record audio from microphone"""
        if filename is None:
            filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        try:
            print(f"🎤 Recording for {duration} seconds...")
            with self.microphone as source:
                audio = self.recognizer.record(source, duration=duration)
            
            # Save audio file
            filepath = os.path.abspath(filename)
            with open(filepath, "wb") as f:
                f.write(audio.get_wav_data())
            
            print(f"✅ Recording saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
    
    def speech_to_text(self, audio_filepath):
        """Convert speech to text using Google Speech Recognition"""
        try:
            with sr.AudioFile(audio_filepath) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"