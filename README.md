# Voice Assistant

A Python-based voice assistant that listens to spoken commands and responds using Google's speech recognition and text-to-speech models — no API key required.

## Features

### Notes & Tasks
- `add note [text]` — saves a note
- `list notes` — reads back saved notes
- `add task [text]` — adds a to-do
- `list tasks` — reads to-dos
- `complete task [number]` — marks a task done

### Reminders
- `remind me to [thing] in [X] minutes` — sets a timed reminder that fires automatically in the background
- `my reminders` — lists upcoming reminders

### Calculator
- `calculate 12 plus 4`
- `what is 10 times 5`

Uses safe math evaluation (no `eval()` on raw user input).

### System & Apps
- `open youtube` / `open gmail` / `open github` — opens websites
- `open whatsapp` — launches apps
- `open [file/folder path]` — opens files or folders
- `take a screenshot` — saves to `Pictures/Screenshots`

### Browser & YouTube Control
- `open chrome` — launches Chrome
- Type, edit, and search directly in the browser's search bar by voice command
- Search on YouTube and click a specific result (e.g. "play 2nd video") by voice command

### Files
- `organize my downloads` — sorts files into Images/Documents/Music/etc.
- `find file [name]` — searches your PC by filename

### Media & System Control
- `set volume to 50`
- `set brightness to 70`
- `play music` — plays the first track in your Music folder

### Info
- `what time is it`
- `what day is it`
- `weather in [city]` — requires a free OpenWeatherMap API key (not set up yet)
- `exit` — quits the assistant

## Requirements

- Python 3.x
- Microphone and speaker access
- Internet connection (used for Google's speech recognition/TTS)

## Installation

```bash
git clone https://github.com/<your-username>/voice-assistant.git
cd voice-assistant
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Then speak any of the commands listed above.

## Notes

- No API key is required for core voice recognition and speech output.
- The optional weather command requires a free [OpenWeatherMap](https://openweathermap.org/api) API key, which is not yet configured.

## License

MIT
