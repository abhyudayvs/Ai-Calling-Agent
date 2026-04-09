# 📞 SmartConnect: AI-Powered Real Estate Receptionist
**Team Name:** LONEWOLF  
**Event:** DevBits'26 | Electronics Engineering Society

## 📖 Overview
SmartConnect is an intelligent "Communication Platform as a Service" (CPaaS) designed for the Real Estate industry. It acts as a Smart Receptionist that handles inbound customer calls, qualifies leads by asking contextual questions (Budget, Location, Type), and automatically generates a Minutes of Meeting (MoM) document for the sales team.

## 🏗️ Architecture
The system uses a WebSocket connection for real-time, low-latency communication (under 2 seconds).



## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Core Server:** FastAPI (WebSockets)
* **Telephony:** Twilio (Programmable Voice)
* **Tunneling:** Ngrok
* **Speech-to-Text (STT):** Faster-Whisper (OpenAI)
* **Brain (LLM):** Google Gemini Pro (LangChain)
* **Text-to-Speech (TTS):** Edge-TTS (Microsoft Azure)
* **Audio Processing:** FFmpeg & Pydub

## 🚀 Setup Instructions
### 1. Installation
```bash
# Clone the repository
git clone [https://github.com/abhyudayvs/Ai-Calling-Agent.git](https://github.com/abhyudayvs/Ai-Calling-Agent.git)
cd Ai-Calling-Agent

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt