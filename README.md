# 🤖 Grude - Personal AI Voice Assistant (Python + Llama3 + SAPI)

A smart, voice-powered personal AI assistant for Windows built with Python. Grude listens to your voice commands, responds in a natural Indian English voice using Microsoft Ravi, and handles everything from opening apps to answering questions — all powered by a local Llama3 AI model. No cloud AI required!

---

## 🚀 Features

* 🎙️ Voice recognition with Indian English support
* 🗣️ Natural Indian English voice (Microsoft Ravi - SAPI5)
* 🤖 AI-powered conversations using local Llama3 (via Ollama)
* 🌦️ Live weather updates for any city
* 📝 Save and read back voice notes
* 📸 Take screenshots and record screen
* 🔊 Control system volume by voice
* 🌐 Open websites and apps by voice
* 🔋 Battery and system info (CPU, RAM)
* 💻 PC control — sleep, restart, shutdown
* 🎵 Random music player
* 🔍 Google search by voice
* 🔒 Secure API key management via `.env`

---

## 🛠️ Tech Stack

* Python 3.11
* SAPI5 — Microsoft Ravi Indian English Voice
* SpeechRecognition — Google Speech API
* Ollama + Llama3 — Local AI Model
* OpenCV — Screen Recording
* PyAutoGUI — Screenshot and Volume Control
* WeatherAPI — Live Weather Data
* psutil — System Info
* python-dotenv — Secure API Key Management

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/nikhilkumar210h-debug/grude-ai.git
cd grude-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Setup

### Step 1 — Create `.env` file:

```
WEATHER_API_KEY=your_weatherapi_key_here
```

Get your free API key from: https://www.weatherapi.com

### Step 2 — Install Ollama + Llama3 (Local AI):

Download Ollama from: https://ollama.com

```bash
ollama pull llama3
ollama serve
```

### Step 3 — Setup Microsoft Ravi Voice

Run in PowerShell as Administrator:

```powershell
$source = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_enIN_RaviM"
$dest   = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enIN_RaviM"
Copy-Item -Path $source -Destination $dest -Recurse -Force
```

---

## ▶️ Usage

Run Grude:

```bash
python main.py
```

Grude will greet you and start listening. Just speak naturally!

---

## 🎙️ Voice Commands

| Say This | Grude Does |
|---|---|
| `What time is it` | Tells current time |
| `What is today's date` | Tells current date |
| `Weather in Mumbai` | Live weather update |
| `Take note buy groceries` | Saves voice note |
| `Read my note` | Reads last saved note |
| `Open YouTube` | Opens YouTube |
| `Open Instagram` | Opens Instagram |
| `Search Python tutorials` | Google search |
| `Play music` | Plays random music |
| `Volume up / Volume down` | Controls volume |
| `Mute` | Mutes system |
| `Screenshot` | Takes screenshot |
| `Record screen` | Records 10 sec video |
| `Battery status` | Battery percentage |
| `CPU usage` | System info |
| `Sleep PC` | Puts PC to sleep |
| `Restart PC` | Restarts with confirmation |
| `Shutdown PC` | Shuts down with confirmation |
| `Goodbye` | Exits Grude |

---

## 📂 Project Structure

```
grude-ai/
│
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not on GitHub)
├── .gitignore           # Files to ignore
├── grude_notes.txt      # Voice notes (auto created)
└── README.md            # This file
```

---

## 🎬 Demo Video

Watch Grude in action:

🔗 Link — 

---

## ⚠️ Requirements

* Windows 10 / 11
* Python 3.10+
* Microphone
* Ollama installed with Llama3 model
* Microsoft Ravi voice (setup steps above)
* Internet connection (weather + speech recognition)

---

## ⚠️ Error Handling

* Handles microphone errors gracefully
* Handles AI timeout and connection errors
* Handles weather API failures with fallback message
* Confirmation required before risky actions (restart, shutdown)

---

## 🔮 Future Improvements

* 🔔 Voice reminders and alarms
* 💬 WhatsApp message sender
* 🌐 GUI dashboard
* 👤 Face recognition login
* 🗣️ Hey Grude hotword detection
* 📧 Email reader
* 🌍 Multi-language support

---

## 🤝 Contributing

Feel free to fork this repo and improve it. Pull requests are welcome!

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 💡 Author

Made with ❤️ by **Nikhil Kumar**
