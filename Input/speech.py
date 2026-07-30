import keyboard
import mouse
from faster_whisper import WhisperModel
import soundcard as sc
import numpy as np
import json
from pathlib import Path


fs = 16000
model = WhisperModel("small", device="cpu")
mic = sc.default_microphone()


#------Push to talk trigger und whisper script------

def listen():

    #--Einstellungen importieren--
    BASE_DIR = Path(__file__).parent.parent
    SETTINGS = BASE_DIR / "data" / "settings.json"
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    #--Einstellungen importieren--

    keyboard.wait(settings["triggerkey"])

    print("🎤 Aufnahme...")

    audio = []

    with mic.recorder(samplerate=fs) as recorder:

        while keyboard.is_pressed(settings["triggerkey"]):
            audio.append(recorder.record(4096))

    if not audio:
        print("❌ Keine Audioaufnahme erkannt.")
        return ""

    audio = np.concatenate(audio, axis=0)

    #print("DEBUG audio:", audio.shape, audio.dtype,
    #      np.min(audio), np.max(audio))

    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    print("🧠 Erkenne Sprache...")

    segments, info = model.transcribe(
        audio,
        language="de",
        initial_prompt="Spotify ist ein Wort. Wachhundmodus ist ein Wort. Du bist ein Sprachassistent. Du bekommst Befehle wie: Bitte öffne Firefox. Häufig vorkommende Wörter sind: Spotify, Firefox, öffne, privat, Browser. Der Sprecher gibt kurze deutsche Computerbefehle. Beispiele: öffne Spotify, öffne Firefox, öffne Firefox privat, öffne Chrome."
    )

    text = "".join(s.text for s in segments)

    print("➡️", text)
    text = text.lower()
    return(text)