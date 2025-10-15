import pickle
import os
import time

class VoiceAuthenticator:
    def __init__(self, state_file="voice_profiles.pkl"):
        self.state_file = state_file
        self.voice_profiles = self.load_voice_profiles()
    
    def load_voice_profiles(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'rb') as f:
                    return pickle.load(f)
            return {}
        except:
            return {}
    
    def save_voice_profiles(self):
        try:
            with open(self.state_file, 'wb') as f:
                pickle.dump(self.voice_profiles, f)
            return True
        except:
            return False
    
    def enroll_user(self, user_id, audio_path):
        """Simple enrollment - just store that user is enrolled"""
        self.voice_profiles[user_id] = {
            'enrolled_at': time.time(),
            'audio_file': audio_path
        }
        success = self.save_voice_profiles()
        if success:
            print(f"✓ User {user_id} enrolled successfully!")
        return success
    
    def authenticate_user(self, user_id, audio_path):
        """Simple authentication - check if user is enrolled"""
        if user_id in self.voice_profiles:
            print(f"✓ User {user_id} authenticated successfully!")
            return True, 1.0
        else:
            print(f"❌ User {user_id} not enrolled")
            return False, 0.0