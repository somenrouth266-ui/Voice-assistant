"""
Command router: takes recognized text, figures out intent, calls the right skill.

Uses simple keyword matching, which is fast, offline, and predictable —
good enough for a personal assistant. Each intent is checked in order;
first match wins, so put more specific patterns first.
"""
import re
from datetime import datetime

import skills.system as system
import skills.notes as notes
import skills.reminders as reminders
import skills.weather as weather
import skills.file_tools as file_tools
import skills.media as media


class CommandRouter:
    def __init__(self, speaker=None):
        self.speaker = speaker

    def handle(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        lower = text.lower()

        # --- Exit ---
        if lower in ("exit", "quit", "goodbye", "stop listening"):
            return "__EXIT__"

        # --- Calculator ---
        m = re.search(r"(?:calculate|what is|what's)\s+(.+)", lower)
        if m and any(ch.isdigit() for ch in m.group(1)):
            expr = self._words_to_math(m.group(1))
            return system.calculate(expr)

        # --- Open website ---
        m = re.search(r"open (?:the website|website)?\s*([\w\.]+\.\w+|\w+)(?:\s+website)?$", lower)
        if "open" in lower and ("website" in lower or "." in lower):
            target = m.group(1) if m else lower.replace("open", "").strip()
            return system.open_website(target)

        # --- Launch app ---
        if lower.startswith("launch ") or lower.startswith("start "):
            app = re.sub(r"^(launch|start)\s+", "", lower)
            return system.launch_app(app)

        # --- Open file/folder ---
        if lower.startswith("open "):
            target = lower.replace("open ", "", 1)
            return system.open_path(target)

        # --- Screenshot ---
        if "screenshot" in lower:
            return system.take_screenshot()

        # --- Notes ---
        m = re.search(r"(?:add note|note that|remember that)\s+(.+)", lower)
        if m:
            return notes.add_note(m.group(1))
        if "list notes" in lower or "read my notes" in lower or "show my notes" in lower:
            return notes.list_notes()

        # --- Todos ---
        m = re.search(r"(?:add task|add to do|add todo|to do)\s+(.+)", lower)
        if m:
            return notes.add_todo(m.group(1))
        if "list tasks" in lower or "my to do" in lower or "my tasks" in lower:
            return notes.list_todos()
        m = re.search(r"(?:complete task|finish task|mark task)\s+(\d+)", lower)
        if m:
            return notes.complete_todo(int(m.group(1)))

        # --- Reminders ---
        m = re.search(r"remind me (?:to |in )?(.+?) in (\d+)\s*minutes?", lower)
        if m:
            message, minutes = m.group(1), int(m.group(2))
            return reminders.add_reminder_in(minutes, message)
        if "my reminders" in lower or "list reminders" in lower:
            return reminders.list_reminders()

        # --- Weather ---
        m = re.search(r"weather(?: in| for)?\s*(.*)", lower)
        if "weather" in lower:
            city = m.group(1).strip() if m else ""
            return weather.get_weather(city or None)

        # --- File search ---
        m = re.search(r"(?:find|search for) (?:file |files )?(.+)", lower)
        if m and "file" in lower:
            return file_tools.search_files(m.group(1).replace("file", "").replace("files", "").strip())

        # --- Organize folder ---
        m = re.search(r"organize (?:my )?(.+)", lower)
        if m:
            return file_tools.organize_folder(m.group(1).strip())

        # --- Music ---
        if "play music" in lower or lower.startswith("play "):
            return media.play_music()

        # --- Volume ---
        m = re.search(r"(?:set )?volume(?: to)? (\d+)", lower)
        if m:
            return media.set_volume(int(m.group(1)))

        # --- Brightness ---
        m = re.search(r"(?:set )?brightness(?: to)? (\d+)", lower)
        if m:
            return media.set_brightness(int(m.group(1)))

        # --- Time ---
        if "what time" in lower or "current time" in lower:
            return f"It's {datetime.now().strftime('%I:%M %p')}."
        if "what day" in lower or "today's date" in lower or "what's the date" in lower:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

        return "Sorry, I didn't understand that command."

    @staticmethod
    def _words_to_math(phrase: str) -> str:
        """Converts spoken math words to symbols, e.g. 'twelve plus four' -> '12 + 4'."""
        replacements = {
            " plus ": " + ", " minus ": " - ", " times ": " * ",
            " multiplied by ": " * ", " divided by ": " / ",
            " x ": " * ",
        }
        for word, symbol in replacements.items():
            phrase = phrase.replace(word, symbol)
        return phrase
