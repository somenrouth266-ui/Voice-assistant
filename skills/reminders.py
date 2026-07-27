"""
Reminders/alarms skill.
Uses SQLite for storage + a background thread that polls every N seconds
and calls the speaker when a reminder's time has come.
"""
import threading
import time
from datetime import datetime, timedelta

from db.database import get_conn


def add_reminder(message: str, remind_at: datetime) -> str:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO reminders (message, remind_at) VALUES (?, ?)",
            (message, remind_at.strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
    return f"Reminder set for {remind_at.strftime('%I:%M %p on %b %d')}: {message}"


def add_reminder_in(minutes: int, message: str) -> str:
    target = datetime.now() + timedelta(minutes=minutes)
    return add_reminder(message, target)


def list_reminders() -> str:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, message, remind_at FROM reminders WHERE fired = 0 ORDER BY remind_at"
        ).fetchall()
    if not rows:
        return "You have no upcoming reminders."
    return "Upcoming reminders: " + "; ".join(
        f"{r['message']} at {r['remind_at']}" for r in rows
    )


def _due_reminders(conn):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return conn.execute(
        "SELECT id, message FROM reminders WHERE fired = 0 AND remind_at <= ?", (now,)
    ).fetchall()


class ReminderChecker:
    """
    Runs in a background thread. Call .start(speaker) from main.py once,
    and it will announce reminders as they come due, for as long as the app runs.
    """

    def __init__(self, poll_seconds: int = 15):
        self.poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread = None

    def start(self, speaker):
        self._thread = threading.Thread(target=self._run, args=(speaker,), daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _run(self, speaker):
        while not self._stop.is_set():
            with get_conn() as conn:
                due = _due_reminders(conn)
                for r in due:
                    speaker.say(f"Reminder: {r['message']}")
                    conn.execute("UPDATE reminders SET fired = 1 WHERE id = ?", (r["id"],))
                if due:
                    conn.commit()
            time.sleep(self.poll_seconds)
