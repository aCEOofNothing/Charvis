import keyboard
import mouse
from faster_whisper import WhisperModel
import soundcard as sc
import numpy as np
import time

from shared import input_queue
from assets import import_settings


fs = 16000
model = WhisperModel("small", device="cpu")
mic = sc.default_microphone()


#------Push to talk trigger und whisper script------

def listen():

    settings = import_settings()

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
    input_queue.put(text)
    return


def short_listen(seconds=5):

    settings = import_settings()

    print("🎤 Aufnahme...")

    audio = []
    end_time = time.monotonic() + seconds
    with mic.recorder(samplerate=fs) as recorder:

        while time.monotonic() < end_time:
            audio.append(recorder.record(4096))
        print("🧠 Erkenne Sprache...")


    if not audio:
        print("❌ Keine Audioaufnahme erkannt.")
        return ""

    audio = np.concatenate(audio, axis=0)

    #print("DEBUG audio:", audio.shape, audio.dtype,
    #      np.min(audio), np.max(audio))

    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    segments, info = model.transcribe(
        audio,
        language="de",
        initial_prompt="Spotify ist ein Wort. Wachhundmodus ist ein Wort. Du bist ein Sprachassistent. Du bekommst Befehle wie: Bitte öffne Firefox. Häufig vorkommende Wörter sind: Spotify, Firefox, öffne, privat, Browser. Der Sprecher gibt kurze deutsche Computerbefehle. Beispiele: öffne Spotify, öffne Firefox, öffne Firefox privat, öffne Chrome."
    )

    text = "".join(s.text for s in segments)

    print("➡️", text)
    text = text.lower()
    input_queue.put(text)
    return