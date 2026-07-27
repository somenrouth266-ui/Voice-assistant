"""
Central configuration for the voice assistant.
Put API keys and paths here so nothing is hardcoded elsewhere.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- Vosk speech recognition ---
# Download a model from https://alphacephei.com/vosk/models
# Small English model (~40MB) is enough to start: vosk-model-small-en-us-0.15
VOSK_MODEL_PATH = str(BASE_DIR / "models" / "vosk-model-en-us-0.22")

# --- Database ---
DB_PATH = str(BASE_DIR / "db" / "assistant.db")

# --- Wake word (set to None to disable, just listen continuously) ---
WAKE_WORD = "hey assistant"

# --- Weather API (https://openweathermap.org/api - free tier) ---
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
WEATHER_DEFAULT_CITY = "Guwahati"

# --- Email (use a Gmail App Password, not your real password) ---
EMAIL_ADDRESS = os.environ.get("ASSISTANT_EMAIL", "")
EMAIL_APP_PASSWORD = os.environ.get("ASSISTANT_EMAIL_PASSWORD", "")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- Audio ---
SAMPLE_RATE = 16000
