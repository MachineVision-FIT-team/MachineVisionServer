# 🎯 Machine Vision NLP Server

**Real-time AI-powered machine communication platform for industrial automation**

A Django-based WebSocket server that enables seamless communication between industrial machines and users through natural language processing and real-time audio transcription.

## 🚀 Key Features

- **Real-time Audio Transcription**: Speech-to-text using Silero and Wav2Vec models
- **Natural Language Analysis**: spaCy-powered text analysis for extracting machine commands
- **Multi-device Support**: WebSocket connections for users and industrial machines
- **API Authentication**: Secure API key system for machine and user access
- **Redis-backed Messaging**: High-performance message queuing and room management
- **Machine State Management**: Track and manage industrial machine status

## 🏗️ System Architecture

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   Client Apps   │◄──────────────►│   Django Server │
│   (Users/UI)    │                 │                 │
└─────────────────┘                 └─────────────────┘
                                             │
┌─────────────────┐    WebSocket    ┌─────────────────┐
│ Industrial      │◄──────────────►│  WebSocket API  │
│ Machines        │                 │   (Consumers)   │
└─────────────────┘                 └─────────────────┘
                                             │
┌─────────────────┐                 ┌─────────────────┐
│ Audio Stream    │────Transcription─►│  NLP Analysis   │
│ (Speech Input)  │                 │  (spaCy + ML)   │
└─────────────────┘                 └─────────────────┘
                                             │
┌─────────────────┐    Real-time    ┌─────────────────┐
│  Redis Message  │◄──────────────►│  Room Manager   │
│     Broker      │                 │  (Channels)     │
└─────────────────┘                 └─────────────────┘
```

## 💼 Perfect for:
- Industrial IoT applications
- Factory automation systems
- Voice-controlled machinery
- Real-time machine monitoring
- Smart manufacturing platforms

## 🛠️ Tech Stack
- **Backend**: Django 5.0, Django Channels, WebSockets
- **AI/ML**: spaCy NLP, Silero STT, Wav2Vec, PyTorch
- **Infrastructure**: Redis, SQLite, Docker-ready
- **Audio**: librosa, soundfile, real-time processing

---

## 🔧 Setup Instructions

### Prerequisites (Python 3.11+)

### 1. Virtual Environment Setup

**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Install NLP Models:**
- Windows: `post_install.bat`
- macOS/Linux: `./post_install.sh`

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Redis Server

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt install redis-server
sudo systemctl start redis-server
```

### 5. Run the Server

```bash
# Local development
python manage.py runserver

# Network access (for mobile/external devices)
python manage.py runserver 0.0.0.0:8000
```

🌐 **Access:** `http://127.0.0.1:8000/` or `http://YOUR_IP:8000`

---

## 🔍 How It Works

1. **Machine Connection**: Industrial machines connect via WebSocket using API keys
2. **Audio Processing**: Real-time speech input gets transcribed using AI models  
3. **NLP Analysis**: spaCy processes text to extract machine commands and objects
4. **Message Routing**: Redis manages real-time communication between components
5. **Response Delivery**: Processed commands sent back to machines and monitoring systems

## 🧠 AI Components

- **Silero STT**: Real-time speech transcription with 16kHz audio processing
- **spaCy NLP**: Natural language understanding for command extraction
- **Semantic Matching**: Intelligent synonym detection for machine vocabulary

## 🚀 Getting Started for Developers

After setup, explore the WebSocket endpoints:
- `/ws/machines/` - Machine device connections
- `/ws/users/` - User interface connections  
- `/ws/api/` - General API WebSocket

**Test with Redis CLI:**
```bash
redis-cli
> ping
PONG
```

Ready to build the future of industrial automation! 🏭
