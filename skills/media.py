"""
Music playback and volume/brightness control.
Volume control is Windows-first (pycaw); falls back gracefully elsewhere.
"""
import platform
import subprocess
from pathlib import Path


def play_music(file_or_folder: str = "~/Music") -> str:
    path = Path(file_or_folder).expanduser()
    if not path.exists():
        return f"I couldn't find '{file_or_folder}'."

    if path.is_dir():
        audio_exts = {".mp3", ".wav", ".flac", ".m4a"}
        tracks = [f for f in path.iterdir() if f.suffix.lower() in audio_exts]
        if not tracks:
            return f"No music files found in {path}."
        path = tracks[0]

    system = platform.system()
    try:
        if system == "Windows":
            import os
            os.startfile(str(path))  # noqa
        elif system == "Darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
        return f"Playing {path.name}"
    except Exception as e:
        return f"Couldn't play music: {e}"


def set_volume(level: int) -> str:
    """level: 0-100"""
    level = max(0, min(100, level))
    system = platform.system()
    try:
        if system == "Windows":
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
        elif system == "Darwin":
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        else:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{level}%"])
        return f"Volume set to {level}%."
    except Exception as e:
        return f"Couldn't change volume: {e}"


def set_brightness(level: int) -> str:
    """level: 0-100"""
    level = max(0, min(100, level))
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return f"Brightness set to {level}%."
    except Exception as e:
        return f"Couldn't change brightness: {e}"
