import soundcard as sc
import numpy as np
from faster_whisper import WhisperModel
import keyboard
import subprocess
import mouse

fs = 16000
model = WhisperModel("small", device="cpu")

mic = sc.default_microphone()

print("Halte SPACE zum Sprechen...")

def handle_command(text):
    text = text.lower()

    if "firefox privat" in text:
        print("🦊 Firefox privat wird gestartet...")
        subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe","-private-window"])

    elif "firefox" in text or "fire fox" in text or "eierfogs" in text:
        print("🦊 Firefox wird gestartet...")
        subprocess.Popen(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])

    elif "whatsapp" in text:
        print("WhatsApp wird gestartet...")
        subprocess.Popen()

    elif "notion" in text:
        print("Notion wird gestartet...")
        subprocess.Popen("C:\\Users\\maels\\AppData\\Local\\Programs\\Notion\\Notion.exe")

    elif "outlook" in text:
        print("C:\\Users\\maels\\AppData\\Local\\Programs\\Notion\\Notion.exe")

    elif "everything" in text or "alles" in text:
        print("Everything wird geöffnet...")
        subprocess.Popen("C:\\Program Files (x86)\\Everything\\Everything.exe")

    elif "spotify" in text:
        print("Spotify wird geöffnet...")
        subprocess.Popen("C:\\Users\\maels\\AppData\\Roaming\\Spotify\\Spotify.exe")

#Japadapadu!

TRIGGER = "start application 2"

while True:
    event = keyboard.read_event()

    if event.name == TRIGGER and event.event_type == keyboard.KEY_DOWN:

        print("🎤 Aufnahme...")

        audio = []

        with mic.recorder(samplerate=fs) as recorder:

            while keyboard.is_pressed(TRIGGER):
                audio.append(recorder.record(4096))

    print("🎤 Aufnahme...")

    if not audio:
        print("❌ Keine Audioaufnahme erkannt. Bitte Space gedrückt halten und erneut sprechen.")
        continue

    audio = np.concatenate(audio, axis=0)
    print("DEBUG audio:", audio.shape, audio.dtype, np.min(audio), np.max(audio))
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    audio = audio.astype(np.float32)

    print("🧠 Erkenne Sprache...")

    segments, info = model.transcribe(
        audio,
        language="de",
        initial_prompt="Spotify ist ein Wort. Du bist ein Sprachassistent. Du bekommst Befehle wie: Bitte öffne Firefox. Häufig vorkommende Wörter sind: Spotify, Firefox, öffne, privat, Browser. Der Sprecher gibt kurze deutsche Computerbefehle. Beispiele: öffne Spotify, öffne Firefox, öffne Firefox privat, öffne Chrome."
    )

    text = "".join(s.text for s in segments)

    print("➡️", text)

    handle_command(text)