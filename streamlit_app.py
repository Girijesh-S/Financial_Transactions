import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import tempfile

from utils.voice_authentication import VoiceAuthenticator
from utils.transaction_processor import TransactionProcessor
from utils.realtime_recorder import RealTimeRecorder

# Page configuration
st.set_page_config(
    page_title="Voice Banking System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def load_components():
    return VoiceAuthenticator(), TransactionProcessor(), RealTimeRecorder()

voice_auth, transaction_processor, recorder = load_components()

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'voice_enrolled' not in st.session_state:
    st.session_state.voice_enrolled = False

def main():
    st.title("🏦 Voice-Activated Banking System")
    st.markdown("Secure banking transactions using voice commands and biometric authentication")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    if not st.session_state.authenticated:
        menu = ["Voice Enrollment", "Login", "About"]
    else:
        menu = ["Banking Dashboard", "Voice Transactions", "Account Settings", "Logout"]
    
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Voice Enrollment":
        show_voice_enrollment()
    elif choice == "Login":
        show_login()
    elif choice == "Banking Dashboard":
        show_dashboard()
    elif choice == "Voice Transactions":
        show_voice_transactions()
    elif choice == "Account Settings":
        show_account_settings()
    elif choice == "About":
        show_about()
    elif choice == "Logout":
        logout()

def show_voice_enrollment():
    st.header("🎤 Voice Enrollment")
    st.info("Enroll your voice for secure biometric authentication")
    
    user_id = st.text_input("User ID", value="user123")
    
    if st.button("Start Voice Enrollment"):
        st.info("🎙️ Please speak the phrase: **'My voice is my password'** clearly into your microphone")
        st.warning("Make sure your microphone is working and you're in a quiet environment")
        
        with st.spinner("🎵 Recording in progress... (4 seconds)"):
            # Use a fixed filename in temp directory
            temp_dir = tempfile.gettempdir()
            audio_file = os.path.join(temp_dir, "enrollment.wav")
            audio_file = recorder.record_audio(duration=4, filename=audio_file)
            
        if audio_file and os.path.exists(audio_file):
            st.success("✅ Recording completed! Processing voice print...")
            
            with st.spinner("🔍 Creating voice embedding..."):
                success = voice_auth.enroll_user(user_id, audio_file)
                
            if success:
                st.success("✅ Voice enrollment successful! Your voice print has been saved.")
                st.session_state.voice_enrolled = True
                st.balloons()
            else:
                st.error("❌ Voice enrollment failed. Possible issues:")
                st.markdown("""
                - Microphone not working
                - Audio too quiet/noisy
                - Speech not clear enough
                - Try again in a quieter environment
                """)
        else:
            st.error("❌ Recording failed. Please check your microphone and try again.")

def show_login():
    st.header("🔐 Secure Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Voice Authentication")
        user_id = st.text_input("User ID", value="user123", key="login_id")
        
        if st.button("Authenticate with Voice"):
            if user_id not in voice_auth.voice_profiles:
                st.error("❌ User not enrolled. Please complete voice enrollment first.")
                return
                
            st.info("🎙️ Please speak: **'My voice is my password'** for authentication")
            
            with st.spinner("🔍 Verifying voice print..."):
                temp_dir = tempfile.gettempdir()
                audio_file = os.path.join(temp_dir, "auth.wav")
                audio_file = recorder.record_audio(duration=4, filename=audio_file)
                
            if audio_file and os.path.exists(audio_file):
                verified, similarity = voice_auth.authenticate_user(user_id, audio_file)
                if verified:
                    st.session_state.authenticated = True
                    st.session_state.current_user = user_id
                    st.success(f"✅ Voice authentication successful! Similarity: {similarity:.2%}")
                    st.balloons()
                else:
                    st.error(f"❌ Voice authentication failed. Similarity: {similarity:.2%}")
            else:
                st.error("❌ Recording failed during authentication")
    
    with col2:
        st.subheader("Manual Login (Fallback)")
        manual_user = st.text_input("Username", value="user123", key="manual_user")
        manual_pin = st.text_input("PIN", type="password", value="1234", key="manual_pin")
        
        if st.button("Manual Login"):
            if manual_user == "user123" and manual_pin == "1234":
                st.session_state.authenticated = True
                st.session_state.current_user = manual_user
                st.success("✅ Manual login successful!")
            else:
                st.error("❌ Invalid credentials")

def show_dashboard():
    st.header("📊 Banking Dashboard")
    
    if not st.session_state.authenticated:
        st.warning("Please login first")
        return
    
    # Account summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Account Balance", f"₹{transaction_processor.account_balance}")
    
    with col2:
        total_transactions = len(transaction_processor.transactions)
        st.metric("Total Transactions", total_transactions)
    
    with col3:
        status = "Enabled" if st.session_state.voice_enrolled else "Not Set"
        st.metric("Voice Auth", status)
    
    # Recent transactions
    st.subheader("Recent Transactions")
    if transaction_processor.transactions:
        df = pd.DataFrame(transaction_processor.transactions)
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.info("No transactions yet")
    
    # Transaction chart
    if transaction_processor.transactions:
        st.subheader("Transaction History")
        df = pd.DataFrame(transaction_processor.transactions)
        fig = px.line(df, x='date', y='balance_after', title='Account Balance Over Time')
        st.plotly_chart(fig, use_container_width=True)

def show_voice_transactions():
    st.header("🎤 Voice Transactions")
    
    if not st.session_state.authenticated:
        st.warning("Please login first")
        return
        
    st.info("Use voice commands for banking transactions")
    
    # Available commands
    st.subheader("Available Voice Commands")
    commands = [
        "💸 **'Transfer [amount] to [recipient]'** - Send money",
        "💰 **'Check balance'** - View account balance", 
        "📋 **'Show transactions'** - View transaction history",
        "🔐 **'Change PIN'** - Update your security PIN using voice"
    ]
    
    for cmd in commands:
        st.write(cmd)
    
    # Voice command interface
    st.subheader("Voice Command Interface")
    
    if st.button("🎤 Start Voice Command"):
        st.info("🎙️ Speak your banking command clearly...")
        
        with st.spinner("🎵 Listening for command... (6 seconds)"):
            temp_dir = tempfile.gettempdir()
            audio_file = os.path.join(temp_dir, "command.wav")
            audio_file = recorder.record_audio(duration=6, filename=audio_file)
            
        if audio_file and os.path.exists(audio_file):
            command_text = recorder.speech_to_text(audio_file)
            
            if command_text and command_text != "Could not understand audio":
                st.success(f"🎯 Command recognized: **'{command_text}'**")
                
                # Process command
                intent = transaction_processor.classify_intent(command_text)
                
                if intent == 'transfer':
                    response = transaction_processor.process_transfer(command_text)
                elif intent == 'balance':
                    response = transaction_processor.check_balance()
                elif intent == 'transactions':
                    response = transaction_processor.show_transactions()
                elif intent == 'change_pin':
                    response = "Please use 'Account Settings' for voice PIN change feature"
                else:
                    response = "Sorry, I didn't understand that command. Try: 'Transfer 500 to John', 'Check balance', or 'Show transactions'"
                
                st.info(f"🤖 {response}")
            else:
                st.error("❌ Could not understand voice command. Please try again.")
        else:
            st.error("❌ Recording failed. Please check your microphone.")

def show_voice_pin_change():
    """Voice-based PIN change interface"""
    st.header("🎤 Change PIN with Voice")
    st.info("Change your security PIN using voice commands")
    
    st.markdown("""
    ### How it works:
    1. **Speak your CURRENT 4-digit PIN** (e.g., say "one two three four")
    2. **Speak your NEW 4-digit PIN** 
    3. **Confirm your new PIN** by speaking it again
    """)
    
    st.warning("🔒 Make sure you're in a private, quiet environment when changing your PIN")
    
    if st.button("🎤 Start Voice PIN Change", type="primary"):
        st.info("🎙️ **Step 1/3:** Please speak your **CURRENT** 4-digit PIN...")
        
        with st.spinner("Recording current PIN..."):
            temp_dir = tempfile.gettempdir()
            current_pin_audio = os.path.join(temp_dir, "current_pin.wav")
            current_pin_audio = recorder.record_audio(duration=4, filename=current_pin_audio)
        
        if current_pin_audio and os.path.exists(current_pin_audio):
            st.success("✅ Current PIN recorded!")
            
            st.info("🎙️ **Step 2/3:** Please speak your **NEW** 4-digit PIN...")
            with st.spinner("Recording new PIN..."):
                new_pin_audio = os.path.join(temp_dir, "new_pin.wav")
                new_pin_audio = recorder.record_audio(duration=4, filename=new_pin_audio)
            
            if new_pin_audio and os.path.exists(new_pin_audio):
                st.success("✅ New PIN recorded!")
                
                st.info("🎙️ **Step 3/3:** Please **CONFIRM** your new 4-digit PIN...")
                with st.spinner("Recording PIN confirmation..."):
                    confirm_pin_audio = os.path.join(temp_dir, "confirm_pin.wav")
                    confirm_pin_audio = recorder.record_audio(duration=4, filename=confirm_pin_audio)
                
                if confirm_pin_audio and os.path.exists(confirm_pin_audio):
                    st.success("✅ PIN confirmation recorded!")
                    
                    # Process all audio files
                    with st.spinner("🔍 Processing PIN change..."):
                        # Convert audio to text
                        current_pin_text = recorder.speech_to_text(current_pin_audio)
                        new_pin_text = recorder.speech_to_text(new_pin_audio)
                        confirm_pin_text = recorder.speech_to_text(confirm_pin_audio)
                        
                        if all([current_pin_text, new_pin_text, confirm_pin_text]):
                            st.write(f"**Recognized:**")
                            st.write(f"- Current PIN: '{current_pin_text}'")
                            st.write(f"- New PIN: '{new_pin_text}'")
                            st.write(f"- Confirm PIN: '{confirm_pin_text}'")
                            
                            # Extract PIN digits
                            current_digits = transaction_processor.extract_pin_from_speech(current_pin_text)
                            new_digits = transaction_processor.extract_pin_from_speech(new_pin_text)
                            confirm_digits = transaction_processor.extract_pin_from_speech(confirm_pin_text)
                            
                            st.write(f"**Extracted PINs:**")
                            st.write(f"- Current: {current_digits}")
                            st.write(f"- New: {new_digits}")
                            st.write(f"- Confirm: {confirm_digits}")
                            
                            # Validate and change PIN
                            if len(new_digits) != 4:
                                st.error(f"❌ PIN must be 4 digits. Got: {new_digits}")
                            elif new_digits != confirm_digits:
                                st.error(f"❌ PINs don't match. New: {new_digits}, Confirm: {confirm_digits}")
                            else:
                                # Verify current PIN and change
                                if transaction_processor.hash_pin(current_digits) == transaction_processor.users['user123']['pin']:
                                    transaction_processor.users['user123']['pin'] = transaction_processor.hash_pin(new_digits)
                                    st.success(f"✅ PIN successfully changed to: {new_digits}")
                                    st.balloons()
                                else:
                                    st.error("❌ Current PIN is incorrect")
                        else:
                            st.error("❌ Could not understand one or more PIN recordings")
                else:
                    st.error("❌ Failed to record PIN confirmation")
            else:
                st.error("❌ Failed to record new PIN")
        else:
            st.error("❌ Failed to record current PIN")

def show_account_settings():
    st.header("⚙️ Account Settings")
    
    if not st.session_state.authenticated:
        st.warning("Please login first")
        return
    
    # Voice PIN Change Section
    show_voice_pin_change()
    
    st.markdown("---")
    
    # Manual PIN Change (Fallback)
    st.subheader("Manual PIN Change (Fallback)")
    col1, col2 = st.columns(2)
    
    with col1:
        old_pin = st.text_input("Current PIN", type="password", key="old_pin")
    with col2:
        new_pin = st.text_input("New PIN", type="password", key="new_pin")
    
    if st.button("Change PIN Manually"):
        if old_pin and new_pin:
            if transaction_processor.change_pin_manual(old_pin, new_pin):
                st.success("✅ PIN changed successfully!")
            else:
                st.error("❌ Current PIN is incorrect")
        else:
            st.error("Please enter both current and new PIN")
    
    st.markdown("---")
    
    # Voice Profile Section
    st.subheader("Voice Profile")
    if st.session_state.voice_enrolled:
        st.success("✅ Voice profile is enrolled")
        if st.button("Re-enroll Voice"):
            st.session_state.voice_enrolled = False
            st.rerun()
    else:
        st.warning("⚠️ Voice profile not enrolled")
        if st.button("Enroll Voice"):
            st.session_state.voice_enrolled = True
            st.rerun()

def show_about():
    st.header("About Voice Banking System")
    st.markdown("""
    ### Features:
    - 🎤 **Voice Biometric Authentication** - Secure login using voice prints
    - 💰 **Voice-Activated Transactions** - Transfer money using voice commands  
    - 🔐 **Voice PIN Change** - Update security PIN using voice
    - 📊 **Real-time Dashboard** - Monitor account activity and balances
    - 🔒 **Dual-Factor Security** - Voice + PIN authentication
    
    ### Voice Commands:
    - **"Transfer 500 to John"** - Send money to recipient
    - **"Check balance"** - View account balance
    - **"Show transactions"** - View transaction history
    - **"Change PIN"** - Update security PIN using voice
    
    ### Technology Stack:
    - **Streamlit** - Web application framework
    - **SpeechRecognition** - Voice-to-text conversion
    - **Audio Processing** - Voice feature extraction
    - **Plotly** - Interactive charts and visualizations
    
    ### Security:
    - Voice biometric authentication
    - PIN-based fallback authentication
    - Secure voice profile storage
    - Encrypted PIN storage
    """)

def logout():
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.success("✅ Logged out successfully!")
    st.rerun()

if __name__ == "__main__":
    main() 