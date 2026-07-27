# Voice Assistant — Setup Guide

## 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

On Linux you also need PortAudio for `sounddevice`/`pyaudio`:
```bash
sudo apt install portaudio19-dev espeak-ng
```
On Windows, `pyttsx3` uses SAPI5 (built in) — nothing extra needed.

## 2. Download the Vosk speech model
Get the small English model (~40MB) from:
https://alphacephei.com/vosk/models

Download `vosk-model-small-en-us-0.15.zip`, unzip it, and place the folder here:
```
voice_assistant/models/vosk-model-small-en-us-0.15/
```

## 3. (Optional) Set up API keys
```bash
# Weather (https://openweathermap.org/api - free tier)
export WEATHER_API_KEY="your_key_here"

# Email (use a Gmail App Password: https://myaccount.google.com/apppasswords)
export ASSISTANT_EMAIL="you@gmail.com"
export ASSISTANT_EMAIL_PASSWORD="your_app_password"
```
On Windows (PowerShell): `$env:WEATHER_API_KEY="your_key_here"`

## 4. Test without a microphone first
```bash
python main.py --text
```
Type commands like `what time is it`, `add note buy milk`, `list notes`, `calculate 12 plus 4`.

## 5. Run with voice
```bash
python main.py
```
By default there's a wake word set in `config.py` (`WAKE_WORD = "hey assistant"`).
Set it to `None` in config.py if you want it always listening without a wake word.

## Example commands
| Say | Does |
|---|---|
| "what time is it" | speaks current time |
| "calculate 12 plus 4" | does math |
| "add note buy groceries" | saves a note |
| "list notes" | reads notes back |
| "add task finish assignment" | adds a to-do |
| "list tasks" | reads to-dos |
| "complete task 1" | marks a to-do done |
| "remind me to call mom in 5 minutes" | sets a reminder |
| "weather in Guwahati" | current weather |
| "open youtube" | opens a website |
| "launch notepad" | opens an app |
| "take a screenshot" | saves a screenshot |
| "organize my downloads" | sorts files by type |
| "find file report" | searches your PC |
| "set volume to 50" | changes system volume |
| "exit" | quits |

## Extending it
Each skill is a plain Python file in `skills/` with functions that take strings
and return strings. To add a new skill:
1. Write the function in a new or existing `skills/*.py` file
2. Add a pattern for it in `skills/router.py`'s `handle()` method

No other wiring needed — `main.py` and the speech layer never change.

## Project structure
```
voice_assistant/
├── main.py                  # entry point, listen/route/speak loop
├── config.py                 # paths, API keys, wake word
├── requirements.txt
├── speech/
│   ├── recognizer.py         # Vosk wrapper (mic -> text)
│   └── speaker.py             # pyttsx3 wrapper (text -> voice)
├── skills/
│   ├── router.py              # intent matching -> dispatches to skills
│   ├── system.py               # calculator, open apps/files/websites, screenshots
│   ├── notes.py                 # notes + to-do list (SQLite)
│   ├── reminders.py              # reminders/alarms + background checker thread
│   ├── weather.py                 # OpenWeatherMap
│   ├── email_skill.py              # smtplib
│   ├── file_tools.py                # organizer + search
│   └── media.py                      # music, volume, brightness
└── db/
    ├── database.py             # SQLite schema + connection helper
    └── assistant.db             # created automatically on first run
```
