"""
Notes and to-do list skill, backed by SQLite.
"""
from db.database import get_conn


# --- Notes ---

def add_note(content: str) -> str:
    with get_conn() as conn:
        conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
    return f"Noted: {content}"


def list_notes() -> str:
    with get_conn() as conn:
        rows = conn.execute("SELECT id, content FROM notes ORDER BY id DESC").fetchall()
    if not rows:
        return "You have no notes."
    return "Your notes: " + "; ".join(f"{r['id']}. {r['content']}" for r in rows)


def delete_note(note_id: int) -> str:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    return f"Deleted note {note_id}." if cur.rowcount else f"No note with id {note_id}."


# --- Todos ---

def add_todo(task: str) -> str:
    with get_conn() as conn:
        conn.execute("INSERT INTO todos (task) VALUES (?)", (task,))
        conn.commit()
    return f"Added to your to-do list: {task}"


def list_todos(include_done: bool = False) -> str:
    query = "SELECT id, task, done FROM todos"
    if not include_done:
        query += " WHERE done = 0"
    query += " ORDER BY id"
    with get_conn() as conn:
        rows = conn.execute(query).fetchall()
    if not rows:
        return "Your to-do list is empty."
    parts = []
    for r in rows:
        mark = "[done] " if r["done"] else ""
        parts.append(f"{r['id']}. {mark}{r['task']}")
    return "Your to-dos: " + "; ".join(parts)


def complete_todo(todo_id: int) -> str:
    with get_conn() as conn:
        cur = conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (todo_id,))
        conn.commit()
    return f"Marked task {todo_id} as done." if cur.rowcount else f"No task with id {todo_id}."


def delete_todo(todo_id: int) -> str:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return f"Deleted task {todo_id}." if cur.rowcount else f"No task with id {todo_id}."
