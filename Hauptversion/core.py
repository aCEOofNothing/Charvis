import soundcard as sc
import numpy as np
from faster_whisper import WhisperModel
import keyboard
import subprocess
import mouse
import json

#------Befehle-Logik-----

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


def handle_command(text):
    orginal_text = text.strip()
    text = orginal_text.lower().strip()
    
    if not text:
        print("fuck you")
        return("fuck you")

    for trigger in ["schreibe", "schreib", "tippe", "tip"]: #Sprech-Einfüg-Funktion
        if text.startswith(trigger):
            print("⌨️ Tippe Text...")
            to_type = orginal_text[len(trigger):].strip().strip(",.?!")
            if to_type:
                keyboard.write(to_type)
                print("⌨️ Text getippt: " + to_type)
            else:
                print("⚠️ Nichts zum Schreiben erkannt")
            return #teständerung

    found = False

    if any(word in text for word in ("gaming", "videospiel", "freizeit")): #Gamingmodus
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

    for keyword, (path, args) in commands.items(): #Einzel-Öffnen

        if keyword in text:
            print(f"🚀 {keyword} wird gestartet...")
            subprocess.Popen([path] + args)
            found = True
            break

    global wachhundmodus

    if "wachhundmodus aus" in text:
        wachhundmodus=False
        print("Wachhundmodus geschlossen")
        found = True

    if "wachhundmodus" in text:
        print("W")
        wachhundmodus=True
        print("Wachhundmodus geöffnet")
        found = True

    if "einstellungen" in text:
        found = True
        print("Schnelleinstellungsmöglichkeiten:"
        "Eingabemodus: Sprache | Text"
        ""
        "-> Um die Einstellungen zu ändern, sage einfach die Einstellungskategurie und die Einstellungsmöglichkeit die du auswählen willst."
        ""
        "Warte auf Antwort... Um das Mnü zu verlassen, sage einfach >Beenden.<")

        if "beenden" in text:
            print("Einstellung geschlossen")
            return
        

    if not found:
        print("❌ Kein passender Befehl gefunden")
        return


def wachhund():
    if wachhundmodus==True:
        print("Wachhund liegt auf der Lauer!")