"""
File organizer (sorts files into folders by type) and file search.
"""
import os
from pathlib import Path

_CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi"},
    "Music": {".mp3", ".wav", ".flac", ".aac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".sql"},
}


def _category_for(ext: str) -> str:
    for category, extensions in _CATEGORY_MAP.items():
        if ext.lower() in extensions:
            return category
    return "Other"


def organize_folder(folder_path: str) -> str:
    folder = Path(folder_path).expanduser()
    if not folder.is_dir():
        return f"'{folder_path}' isn't a valid folder."

    moved = 0
    for item in folder.iterdir():
        if item.is_file():
            category = _category_for(item.suffix)
            dest_dir = folder / category
            dest_dir.mkdir(exist_ok=True)
            try:
                item.rename(dest_dir / item.name)
                moved += 1
            except Exception:
                continue

    return f"Organized {moved} files in {folder.name} into category folders." if moved else "Nothing to organize — folder is already tidy or empty."


def search_files(query: str, search_dir: str = "~", max_results: int = 15) -> str:
    root = Path(search_dir).expanduser()
    query_lower = query.lower()
    matches = []

    for dirpath, dirnames, filenames in os.walk(root):
        # skip hidden/system dirs for speed
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fname in filenames:
            if query_lower in fname.lower():
                matches.append(str(Path(dirpath) / fname))
                if len(matches) >= max_results:
                    break
        if len(matches) >= max_results:
            break

    if not matches:
        return f"No files found matching '{query}'."
    return f"Found {len(matches)} file(s): " + "; ".join(matches)
