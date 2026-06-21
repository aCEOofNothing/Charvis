#-----Grundanweisungen-----

import soundcard as sc
import numpy as np
from faster_whisper import WhisperModel
import keyboard
import subprocess
import mouse

fs = 16000
model = WhisperModel("small", device="cpu")

mic = sc.default_microphone()

print("Halte NUMPAD-0 zum Sprechen...")


#------Einstellungen------

settings = {
    "trigger_key": "num 0"
}
#noch nirgends verwendet


#------Befehle-Logik-----

def handle_command(text):
    genauer_text = text.strip()
    text = text.lower().strip()
    commands = {
        "firefox privat": ("C:\\Program Files\\Mozilla Firefox\\firefox.exe", ["-private-window"]),
        "firefox": ("C:\\Program Files\\Mozilla Firefox\\firefox.exe", []),
        "whatsapp": (None, []),
        "notion": ("C:\\Users\\maels\\AppData\\Local\\Programs\\Notion\\Notion.exe", []),
        "outlook": (None, []),
        "everything": ("C:\\Program Files (x86)\\Everything\\Everything.exe", []),
        "spotify": ("C:\\Users\\maels\\AppData\\Roaming\\Spotify\\Spotify.exe", []),
        "explorer": ("C:\\Windows\\explorer.exe",[]),
        "signal": ("C:\\Users\\maels\\AppData\\Local\\Programs\\signal-desktop\\Signal.exe", []),
        "cortex": ("C:\\Program Files (x86)\\Razer\\Razer Cortex\\RazerCortex.exe", []),
        "steam": ("C:\\Program Files (x86)\\Steam\\steam.exe", []),
        "terminal": ("C:\\Program Files\\WindowsApps\\Microsoft.WindowsTerminal_1.24.11321.0_x64__8wekyb3d8bbwe\\WindowsTerminal.exe", []),
        "vscode": ("C:\\Users\\maels\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", []),
        "da vinci resolve": ("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Blackmagic Design\\DaVinci Resolve\\DaVinci Resolve.lnk", [])
    }

    for trigger in ["schreibe", "schreib", "tippe", "tip"]:
        if text.startswith(trigger):
            print("⌨️ Tippe Text...")
            to_type = genauer_text[len(trigger):].strip().strip(",.?!")

            if to_type:
                keyboard.write(to_type)
                print("⌨️ Text getippt: " + to_type)
            else:
                print("⚠️ Nichts zum Schreiben erkannt")

            return

    found = False

    if any(word in text for word in ("gaming", "videospiel", "freizeit")):
        print("🎮 Gamingmodus wird gestartet...")

        gaming_apps = [
              "steam",
             "spotify",
             "cortex"
        ]

        for app in gaming_apps:
                 
            if app not in commands:
                print(f"❌ {app} existiert nicht im commands-Dictionary")
                continue

            path, args = commands[app]

            print(f"🚀 Starte {app}")
            subprocess.Popen([path] + args)

        return

    for keyword, (path, args) in commands.items():

        if keyword in text:
            print(f"🚀 {keyword} wird gestartet...")
            subprocess.Popen([path] + args)
            found = True
            break

    if not found:
        print("❌ Kein passender Befehl gefunden")


#------Push to talk trigger und whisper script------

while True:
    keyboard.wait("num 0")

    print("🎤 Aufnahme...")

    audio = []

    with mic.recorder(samplerate=fs) as recorder:

        while keyboard.is_pressed("num 0"):
            audio.append(recorder.record(4096))

    if not audio:
        print("❌ Keine Audioaufnahme erkannt.")
        continue

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
        initial_prompt="Spotify ist ein Wort. Du bist ein Sprachassistent. Du bekommst Befehle wie: Bitte öffne Firefox. Häufig vorkommende Wörter sind: Spotify, Firefox, öffne, privat, Browser. Der Sprecher gibt kurze deutsche Computerbefehle. Beispiele: öffne Spotify, öffne Firefox, öffne Firefox privat, öffne Chrome."
    )

    text = "".join(s.text for s in segments)

    print("➡️", text)

    handle_command(text)
    
    print("------")





#Japadapadu!