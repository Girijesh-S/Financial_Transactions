# Voice-Activated Banking System 🏦🎤

This project is a **Voice-Activated Banking System** that allows customers to perform banking transactions using voice commands with biometric voice authentication. The admin can view all transactions and manage user accounts through a comprehensive dashboard.

## Features 🛠️

### 1. **Voice Biometric Authentication** 🔐
   - **Voice Enrollment**: 
     - Users can enroll their voice prints for secure authentication
     - System creates unique voice embeddings for each user
   - **Two-Factor Authentication**:
     - Voice print verification + PIN authentication
     - Fallback to manual PIN login if voice recognition fails

### 2. **Voice-Activated Transactions** 💰
   - **Voice Commands**:
     - **"Transfer [amount] to [recipient]"** - Send money using voice
     - **"Check balance"** - View account balance
     - **"Show transactions"** - View transaction history
     - **"Change PIN"** - Update security PIN using voice
   - **Real-time Processing**:
     - Instant voice-to-text conversion
     - Automated transaction processing

### 3. **Admin Dashboard** 🖥️
   - **Admin Login** 🔑:
     - The admin can log in using the credentials:
       - **Username**: `Girijesh` 🧑‍💼
       - **Password**: `User1` 🔒
       - **Username**: `Hari` 👨‍💼  
       - **Password**: `User2` 🔒
   - **Dashboard** 📊:
     - Real-time transaction monitoring
     - Account balance tracking
     - Voice authentication analytics
     - Interactive charts and visualizations

## Technologies Used 🧑‍💻

### Frontend 🌐:
   - **Streamlit**: Modern web application framework for ML and Data Science Projects

### Backend 🔙:
   - **Streamlit**: Handles both frontend and backend seamlessly
   - **Session State Management**: User authentication and data persistence
   - **Audio Processing**: Real-time voice recording and processing

### Voice Technology 🎤:
   - **SpeechRecognition**: Google Speech-to-Text API integration
   - **PyAudio**: Real-time audio recording from microphone
   - **Voice Biometrics**: Custom voice feature extraction and matching
   - **Audio Processing**: WAV file handling and feature extraction

## How to Run the Project 🚀

### 1. **Install Dependencies** 🛠️:
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/Girijesh-S/Financial_Transactions.git
     ```
   - Navigate to the project folder:
     ```bash
     cd Financial_Transactions
     ```
   - Install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

### 2. **Run the Streamlit Application** 🏃‍♂️:
   - Start the Streamlit server:
     ```bash
     streamlit run streamlit_app.py
     ```
   - The application will automatically open in your browser at `http://localhost:8501`.

### 3. **First-Time Setup** ⚙️:
   1. **Voice Enrollment**: Navigate to "Voice Enrollment" and record your voice print
   2. **Login**: Use voice authentication or manual PIN login
   3. **Start Banking**: Begin using voice commands for transactions

## Voice Command Examples 🎯

### Banking Transactions:
```bash
"Transfer 500 to John"
"Check my balance" 
"Show last 5 transactions"
"Change my PIN"
