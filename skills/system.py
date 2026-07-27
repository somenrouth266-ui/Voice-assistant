"""
System-level skills: calculator, opening websites/apps/files, screenshots.
"""
import ast
import operator
import os
import platform
import subprocess
import webbrowser
from pathlib import Path


# --- Calculator (safe eval via AST, no raw eval()) ---

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed")
    if isinstance(node, ast.BinOp):
        op_func = _OPS.get(type(node.op))
        if not op_func:
            raise ValueError("Unsupported operation")
        return op_func(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op_func = _OPS.get(type(node.op))
        if not op_func:
            raise ValueError("Unsupported operation")
        return op_func(_eval_node(node.operand))
    raise ValueError("Unsupported expression")


def calculate(expression: str) -> str:
    """
    Safely evaluates a math expression like '12 * (3 + 4)'.
    Never uses raw eval() — parses to an AST and only allows arithmetic.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"{expression} equals {result}"
    except ZeroDivisionError:
        return "That's a division by zero, which isn't possible."
    except Exception:
        return f"Sorry, I couldn't calculate '{expression}'."


# --- Open websites ---

_KNOWN_SITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chat.openai.com",
}


def open_website(name_or_url: str) -> str:
    key = name_or_url.strip().lower()
    url = _KNOWN_SITES.get(key)
    if not url:
        url = name_or_url if name_or_url.startswith("http") else f"https://{name_or_url}"
    webbrowser.open(url)
    return f"Opening {name_or_url}"


# --- Open files / folders ---

def open_path(path: str) -> str:
    p = Path(path).expanduser()
    if not p.exists():
        return f"I couldn't find '{path}'."
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(str(p))  # noqa
        elif system == "Darwin":
            subprocess.Popen(["open", str(p)])
        else:
            subprocess.Popen(["xdg-open", str(p)])
        return f"Opening {p.name}"
    except Exception as e:
        return f"Couldn't open '{path}': {e}"


# --- Launch applications ---

_APP_ALIASES = {
    "Windows": {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
    },
    "Darwin": {
        "notes": "Notes",
        "calculator": "Calculator",
        "terminal": "Terminal",
        "finder": "Finder",
    },
    "Linux": {
        "files": "nautilus",
        "terminal": "gnome-terminal",
        "text editor": "gedit",
    },
}


def launch_app(app_name: str) -> str:
    system = platform.system()
    aliases = _APP_ALIASES.get(system, {})
    target = aliases.get(app_name.strip().lower(), app_name)
    try:
        if system == "Windows":
            subprocess.Popen(target, shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", target])
        else:
            subprocess.Popen([target])
        return f"Launching {app_name}"
    except Exception as e:
        return f"Couldn't launch '{app_name}': {e}"


# --- Screenshots ---

def take_screenshot(save_dir: str = "~/Pictures/Screenshots") -> str:
    try:
        import pyautogui
        from datetime import datetime

        out_dir = Path(save_dir).expanduser()
        out_dir.mkdir(parents=True, exist_ok=True)
        filename = out_dir / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img = pyautogui.screenshot()
        img.save(str(filename))
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Couldn't take a screenshot: {e}"
