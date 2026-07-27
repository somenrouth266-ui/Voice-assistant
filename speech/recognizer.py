"""
Wraps Vosk so the rest of the app just calls recognizer.listen() and gets text back.
"""
import json
import queue
import sys

import sounddevice as sd
from vosk import Model, KaldiRecognizer

import config


class Recognizer:
    def __init__(self, model_path: str = None, sample_rate: int = None):
        self.sample_rate = sample_rate or config.SAMPLE_RATE
        model_path = model_path or config.VOSK_MODEL_PATH
        try:
            self.model = Model(model_path)
        except Exception as e:
            print(f"[Recognizer] Failed to load Vosk model at '{model_path}'.")
            print("Download one from https://alphacephei.com/vosk/models and unzip it there.")
            raise e

        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self.audio_q = queue.Queue()

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(f"[Recognizer] audio status: {status}", file=sys.stderr)
        self.audio_q.put(bytes(indata))

    def listen_once(self, timeout: float = 8.0) -> str:
        """
        Opens the mic, listens until a pause is detected (or timeout), returns recognized text.
        Blocking call — meant to be run in the main loop, not on every audio frame.
        """
        self.rec.Reset()
        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            print("[Recognizer] listening...")
            silence_chunks = 0
            while True:
                data = self.audio_q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        return text
                    silence_chunks += 1
                else:
                    partial = json.loads(self.rec.PartialResult())
                    # Optional: print partial for live feedback
                    # print(partial.get("partial", ""), end="\r")
                if silence_chunks > timeout:
                    return ""
