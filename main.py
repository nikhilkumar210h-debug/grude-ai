# ============================================================
# GRUDE - Personal AI Voice Assistant
# Made by: Nikhil Kumar
# Description: A voice-based AI assistant for Windows
#              with Indian English voice (Microsoft Ravi)
# ============================================================

# ── Standard Library Imports ──
import os
import re
import time
import glob
import random
import webbrowser
from datetime import datetime

# ── Third Party Imports ──
import cv2
import numpy as np
import psutil
import pyautogui
import requests
import speech_recognition as sr
import win32com.client
import groq as groq_lib
from dotenv import load_dotenv

# ── Load Environment Variables (.env file) ──
load_dotenv()

# ============================================================
# VOICE SETUP - Microsoft Ravi (Indian English)
# ============================================================
speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()
speaker.Voice = voices.Item(1)  # Index 1 = Microsoft Ravi
speaker.Rate = 0                # Speed: -10 to 10
speaker.Volume = 100            # Volume: 0 to 100

# ============================================================
# CONSTANTS
# ============================================================
USER_NAME = "Nikhil"
OLLAMA_URL = "http://localhost:11434/api/chat"
AI_MODEL = "llama3"
MUSIC_FOLDER = r"E:\music"

# ── AI Mode Tracker ──
ai_mode = "cloud"


# ============================================================
# CORE FUNCTIONS
# ============================================================

def say(text):
    """Speak text using Microsoft Ravi voice"""
    print(f"Grude: {text}")
    text = str(text)
    text = text.replace("*","").replace("#","").replace("_","")
    text = text.replace("`","").replace("|","").replace("~","")
    text = text.replace("&", "and").replace("%", "percent")
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\n+', ' ', text).strip()
    if len(text) > 400:
        text = text[:400] + "."
    if not text.strip():
        return
    speaker.Speak(text)


def take_command():
    """Listen to microphone and return recognized text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-IN")
            print(f"You: {query}")
            return query.lower()
        except:
            return ""


# ============================================================
# TIME & DATE
# ============================================================

def tell_time():
    """Tell current time"""
    now = datetime.now()
    say(f"Current time is {now.strftime('%I:%M %p')}")


def tell_date():
    """Tell current date"""
    now = datetime.now()
    say(f"Today is {now.strftime('%A, %d %B %Y')}")


# ============================================================
# SYSTEM CONTROL
# ============================================================

def sleep_pc():
    """Put PC to sleep"""
    say("Going to sleep")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def restart_pc():
    """Restart PC after 5 seconds"""
    say("Restarting your PC in 5 seconds.")
    time.sleep(5)
    os.system("shutdown /r /t 0")


def shutdown_pc():
    """Shutdown PC after 5 seconds"""
    say("Shutting down your PC in 5 seconds.")
    time.sleep(5)
    os.system("shutdown /s /t 0")


def tell_battery():
    """Tell battery percentage and charging status"""
    battery = psutil.sensors_battery()
    if battery:
        percent = int(battery.percent)
        plugged = "charging" if battery.power_plugged else "not charging"
        say(f"Battery is at {percent} percent and {plugged}.")
    else:
        say("Could not detect battery.")


def tell_system_info():
    """Tell CPU and RAM usage"""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    say(f"CPU usage is {cpu} percent and RAM usage is {ram} percent.")


# ============================================================
# SCREEN FUNCTIONS
# ============================================================

def take_screenshot():
    """Take a screenshot and save it"""
    name = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
    img = pyautogui.screenshot()
    img.save(name)
    say(f"Screenshot saved as {name}")


def record_screen(duration=10):
    """Record screen for given duration in seconds"""
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("recording.avi", fourcc, 20.0, screen_size)
    say("Recording started")
    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()
    say("Recording saved")


# ============================================================
# NOTES
# ============================================================

def take_note(query):
    """Save a voice note to grude_notes.txt"""
    note = query.replace("take note", "").replace("note down", "").replace("note", "").strip()
    if not note:
        say("What should I note down?")
        note = take_command()
    if note:
        with open("grude_notes.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')} - {note}\n")
        say(f"Note saved: {note}")
    else:
        say("Nothing to save.")


def open_last_note():
    """Read the last saved note"""
    try:
        with open("grude_notes.txt", "r") as f:
            lines = f.readlines()
        if lines:
            say(f"Your last note is: {lines[-1].strip()}")
        else:
            say("No notes found.")
    except FileNotFoundError:
        say("You have not saved any notes yet.")


# ============================================================
# WEATHER
# ============================================================

def get_weather(city="dehri on sone"):
    """Fetch and speak current weather for given city"""
    API_KEY = os.getenv("WEATHER_API_KEY")
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data["current"]["temp_c"]
        desc = data["current"]["condition"]["text"]
        feels = data["current"]["feelslike_c"]
        say(f"{USER_NAME}, the weather in {city} is {desc}.")
        say(f"Temperature is {temp} degrees, feels like {feels} degrees.")
        if temp > 35:
            say("It is quite hot. Please take care and drink water.")
        elif temp < 15:
            say("It is cold outside. Stay warm.")
        else:
            say("The weather feels comfortable today.")
    except:
        say(f"Sorry {USER_NAME}, I could not fetch the weather.")


# ============================================================
# MUSIC
# ============================================================

def play_music():
    """Play a random MP3 from the music folder"""
    songs = glob.glob(f"{MUSIC_FOLDER}\\*.mp3")
    if songs:
        os.startfile(random.choice(songs))
        say("Playing music")
    else:
        say("No music files found")


# ============================================================
# WEB & SEARCH
# ============================================================

def google_search(query):
    """Search Google with the given query"""
    search_query = query.replace("search", "").replace("google", "").strip()
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
    say(f"Searching for {search_query}")


# Sites and their trigger keywords
sites = {
    "youtube":   ["open youtube",   "launch youtube",   "go to youtube"],
    "google":    ["open google",    "launch google",    "go to google"],
    "instagram": ["open instagram", "launch instagram"],
    "wikipedia": ["open wikipedia", "launch wikipedia"],
    "chatgpt":   ["open chatgpt",   "chat gpt",         "open chat gpt"],
    "pycharm":   ["open pycharm",   "open python",      "open code writer"]
}

links = {
    "youtube":   "https://www.youtube.com/",
    "google":    "https://www.google.com/",
    "instagram": "https://www.instagram.com/",
    "wikipedia": "https://www.wikipedia.org/",
    "chatgpt":   "https://chat.openai.com/"
}


# ============================================================
# APP LAUNCHER
# ============================================================

def open_app(app_name):
    """Open a Windows application by name"""
    apps = {
        "brave":      r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "notepad":    "notepad.exe",
        "calculator": "calc.exe",
        "wordpad":    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "game":       r"D:\Horizon Zero Dawn\HorizonZeroDawn.exe",
        "pycharm":    r"C:\Program Files\JetBrains\PyCharm Community Edition 2025.2.6\bin\pycharm64.exe"
    }
    for name, path in apps.items():
        if name in app_name:
            try:
                os.startfile(path)
                return f"Opened {name}"
            except:
                return "App not found or path issue"
    return "App not recognized"


# ============================================================
# AI - SMART CLOUD + LOCAL FALLBACK
# ============================================================

def create_system_message():
    """Create the AI system prompt"""
    return {
        "role": "system",
        "content": """
You are Grude, a smart, calm, and helpful AI assistant.

The user's name is Nikhil. He is your boss.
Always respect him, but do not overuse his name.

Speak only in English.

Your communication style:
- Be clear, simple, and natural (like a real human assistant)
- Give short answers first, then explain if needed
- Be polite and respectful
- Show light emotion when appropriate (friendly, caring, calm)
- Do not sound robotic
- Never use bullet points, markdown, or symbols.
- Always reply in maximum 2-3 short sentences.
- Never introduce yourself with a feature list.
- Speak naturally like a human assistant.

Behavior rules:
- If the user asks a question → answer clearly with example if needed
- If the user gives a command → respond confidently and act
- If you don't understand → politely ask for clarification
- If something fails → say sorry and try to help again
- If the user seems casual → respond casually
- If the user is serious → respond more professionally

Identity:
- If asked "who are you" or "what are you" → say: "I am Grude, your personal AI assistant made by Nikhil."
- If asked "who am I" or "who is my boss" → say: "You are Nikhil, my user and my boss."
- Never confuse these two questions.

App control:
- Reply with ACTION:open_app ONLY when user says "open", "launch", or "start" followed by an app name.
- NEVER use ACTION format for any other type of question or command.

Example:
User: open notepad → ACTION:open_app:notepad
User: who are you → I am Grude, your personal AI assistant.
Otherwise: Respond normally like a smart human assistant.
"""
    }


def check_groq_available():
    """Check if Groq cloud API is available"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ No Groq API key")
        return False
    try:
        client = groq_lib.Groq(api_key=api_key)
        client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print("✅ Groq test success!")
        return True
    except groq_lib.RateLimitError:
        print("❌ Groq rate limit")
        return False
    except groq_lib.AuthenticationError:
        print("❌ Wrong Groq API key")
        return False
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return False


def get_cloud_reply(messages):
    """Get AI reply from Groq cloud"""
    api_key = os.getenv("GROQ_API_KEY")
    client = groq_lib.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content


def get_local_reply(messages):
    """Get AI reply from local Ollama"""
    data = {
        "model": AI_MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=data, timeout=30)
    return response.json()["message"]["content"]


def get_ai_reply(messages):
    """Smart AI — tries cloud first, falls back to local"""
    global ai_mode

    if ai_mode == "cloud":
        try:
            reply = get_cloud_reply(messages)
            print("🌐 [Cloud AI - Groq]")
            return reply
        except groq_lib.RateLimitError:
            print("⚠️ Cloud limit — switching to Local")
            say("Switching to local AI.")
            ai_mode = "local"
        except Exception as e:
            print(f"⚠️ Cloud error: {e}")
            ai_mode = "local"

    if ai_mode == "local":
        try:
            reply = get_local_reply(messages)
            print("💻 [Local AI - Llama3]")
            return reply
        except Exception as e:
            raise Exception(f"Both AI unavailable: {e}")


def handle_ai_response(reply):
    """Handle ACTION commands from AI"""
    if reply.startswith("ACTION:open_app:"):
        app = reply.split(":")[-1]
        result = open_app(app)
        say(result)
        return True
    return False


def trim_memory(messages):
    """Keep only last 18 messages"""
    if len(messages) > 20:
        return messages[:1] + messages[-18:]
    return messages


def check_ai_on_startup():
    """Check which AI is available on startup"""
    global ai_mode

    api_key = os.getenv("GROQ_API_KEY")
    print(f"🔑 Groq Key: {api_key[:10] if api_key else 'NOT FOUND'}")

    cloud_ok = check_groq_available()
    local_ok = False

    try:
        requests.get("http://localhost:11434", timeout=2)
        local_ok = True
    except:
        local_ok = False

    print(f"☁️ Cloud OK: {cloud_ok} | 💻 Local OK: {local_ok}")

    if cloud_ok:
        ai_mode = "cloud"
        print("🌐 Cloud AI ready (Groq)")
        say("Cloud AI is ready.")
    elif local_ok:
        ai_mode = "local"
        print("💻 Local AI ready (Ollama)")
        say("Local AI is ready.")
    else:
        print("❌ No AI available!")
        say("Warning. No AI is available. Please start Ollama or check internet.")


# ============================================================
# MAIN CHAT LOOP
# ============================================================

def chat():
    """Main loop - listen for commands and respond"""
    messages = [create_system_message()]

    while True:
        query = take_command()
        if not query:
            continue

        # ── Exit ──
        if "exit" in query or "stop" in query or "goodbye" in query:
            say("Goodbye sir. Have a great day.")
            break

        # ── Open Websites ──
        opened = False
        for site, keywords in sites.items():
            for word in keywords:
                if word in query:
                    webbrowser.open(links[site])
                    say(f"Opening {site}")
                    opened = True
                    break
            if opened:
                break
        if opened:
            continue

        # ── Time & Date ──
        if "time" in query:
            tell_time()
            continue
        if "date" in query:
            tell_date()
            continue

        # ── Weather ──
        if "weather" in query or "mausam" in query:
            words = query.split()
            city = "dehri on sone"
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = " ".join(words[idx + 1:])
            get_weather(city)
            continue

        # ── Volume Control ──
        if "volume up" in query:
            pyautogui.press('volumeup', presses=5)
            say("Volume increased")
            continue
        if "volume down" in query:
            pyautogui.press('volumedown', presses=5)
            say("Volume decreased")
            continue
        if "mute" in query:
            pyautogui.press('volumemute')
            say("Muted")
            continue

        # ── Notes ──
        if "open my note" in query or "open last note" in query or \
           "read note" in query or "read my note" in query or \
           "show note" in query or "my note" in query:
            open_last_note()
            continue

        if ("take note" in query or "note down" in query) or \
           ("note" in query and "notepad" not in query and
                "open" not in query and "read" not in query and
                "last" not in query and "my" not in query and
                "show" not in query):
            take_note(query)
            continue

        # ── PC Power Control ──
        if "restart pc" in query:
            say("Are you sure you want to restart?")
            confirm = take_command()
            restart_pc() if "yes" in confirm or "restart" in confirm else say("Restart cancelled.")
            continue

        if "shutdown pc" in query or "shut down pc" in query:
            say("Are you sure you want to shutdown?")
            confirm = take_command()
            shutdown_pc() if "yes" in confirm or "shutdown" in confirm else say("Shutdown cancelled.")
            continue

        if "sleep pc" in query:
            sleep_pc()
            continue

        # ── Screen ──
        if "record screen" in query:
            record_screen(10)
            continue
        if "screenshot" in query:
            take_screenshot()
            continue

        # ── Direct App Open ──
        if "open notepad" in query:
            os.startfile("notepad.exe")
            say("Opening Notepad")
            continue
        if "open calculator" in query or "open calc" in query:
            os.startfile("calc.exe")
            say("Opening Calculator")
            continue

        # ── System Info ──
        if "battery" in query:
            tell_battery()
            continue
        if "system info" in query or "cpu usage" in query or "ram usage" in query:
            tell_system_info()
            continue

        # ── Google Search ──
        if "search" in query or "google search" in query:
            google_search(query)
            continue

        # ── Music ──
        if "play music" in query:
            play_music()
            continue

        # ── AI Response ──
        messages.append({"role": "user", "content": query})
        try:
            reply = get_ai_reply(messages)

            if "ACTION:open_app" in reply:
                if "open" in query:
                    if handle_ai_response(reply):
                        continue
                else:
                    reply = reply.replace(reply[reply.find("ACTION"):], "").strip()
                    if not reply:
                        reply = "Sure, how can I help you?"

            say(reply)
            messages.append({"role": "assistant", "content": reply})
            messages = trim_memory(messages)

        except Exception as e:
            print(f"Error: {e}")
            say("Sorry, something went wrong.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    say("Hello sir, I am Grude. How can I help you today?")
    check_ai_on_startup()
    chat()