"""
Speaks using Windows SAPI5 directly via pywin32.
More reliable than pyttsx3 on Windows, which can silently stop
producing audio after the first call.
"""
import win32com.client


class Speaker:
    def __init__(self, rate: int = 0, volume: int = 100, voice_index: int = None):
        self.engine = win32com.client.Dispatch("SAPI.SpVoice")
        self.engine.Rate = rate  # -10 (slow) to 10 (fast), 0 = normal
        self.engine.Volume = volume  # 0-100
        if voice_index is not None:
            voices = self.engine.GetVoices()
            if 0 <= voice_index < voices.Count:
                self.engine.Voice = voices.Item(voice_index)

    def say(self, text: str):
        print(f"[Assistant] {text}")
        self.engine.Speak(text)

    def list_voices(self):
        voices = self.engine.GetVoices()
        for i in range(voices.Count):
            print(i, voices.Item(i).GetDescription())