"""
Voice Assistant — main entry point.

Run modes:
    python main.py            -> voice mode (mic in, speaker out)
    python main.py --text     -> text mode (type commands, useful for testing without a mic)
"""
import sys

from db.database import init_db
from skills.router import CommandRouter
from skills.reminders import ReminderChecker
import config


def run_text_mode():
    from speech.speaker import Speaker
    speaker = Speaker()
    router = CommandRouter(speaker)

    checker = ReminderChecker()
    checker.start(speaker)

    print("Voice Assistant (text mode). Type 'exit' to quit.\n")
    speaker.say("Hello! I'm ready. Type a command.")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not text:
            continue
        response = router.handle(text)
        if response == "__EXIT__":
            speaker.say("Goodbye!")
            break
        speaker.say(response)

    checker.stop()


def run_voice_mode():
    from speech.recognizer import Recognizer
    from speech.speaker import Speaker

    speaker = Speaker()
    recognizer = Recognizer()
    router = CommandRouter(speaker)

    checker = ReminderChecker()
    checker.start(speaker)

    speaker.say("Hello! I'm listening.")

    while True:
        text = recognizer.listen_once()
        if not text:
            continue
        print(f"You said: {text}")

        # Optional wake word gating
        if config.WAKE_WORD and config.WAKE_WORD not in text.lower():
            continue
        if config.WAKE_WORD:
            text = text.lower().replace(config.WAKE_WORD, "").strip()

        response = router.handle(text)
        if response == "__EXIT__":
            speaker.say("Goodbye!")
            break
        speaker.say(response)

    checker.stop()


if __name__ == "__main__":
    init_db()
    if "--text" in sys.argv:
        run_text_mode()
    else:
        run_voice_mode()
