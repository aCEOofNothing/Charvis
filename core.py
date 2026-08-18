





# "Abbrechen"-Funktion muss gefixt werden








import keyboard
import subprocess
import mouse
import json
from pathlib import Path
import pyautogui
import ctypes
import os
import json

from modules.befehl_zu_bestimmter_tastendruck_modul.befehl_zu_bestimmter_tastendruck import befehl_zu_bestimmter_tastendruck


#------Einstellungen importieren------

def import_settings(path):
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR/path
    with open(SETTINGS, "r") as file:
        settings = json.load(file)
    return settings

def save_settings(path, settings):
    BASE_DIR = Path(__file__).parent
    SETTINGS = BASE_DIR/path
    with open(SETTINGS, "w") as file:
        json.dump(settings, file, indent=4)


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

    found = False

    for trigger in ["schreibe", "schreib", "tippe", "tip"]: #Sprech-Einfüg-Funktion
        if text.startswith(trigger):
            found = True
            print("⌨️ Tippe Text...")
            to_type = orginal_text[len(trigger):].strip().strip(",.?!")
            if to_type:
                keyboard.write(to_type)
                print("⌨️ Text getippt: " + to_type)
            else:
                print("⚠️ Nichts zum Schreiben erkannt")
            return #teständerung

    if "hallo" in text: #Hallo sagen
        found = True
        return("Hallo Meister!")

    if "komandowort" in text:
        found = True
        wakeword = import_settings("data/settings.json")["wakeword"]
        print(wakeword)
        if wakeword == True:
            print("True")
            return
        elif wakeword == False:
            print("False")
            return
        else:
            print("Nix")
            return

    if any(word in text for word in ("gaming", "videospiel", "freizeit")): #Gamingmodus
        found = True
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

    #Kritische Systembefehle:
    if "pc" in text:
        if "herunterfahren" in text:
            subprocess.run(["shutdown", "/s", "/t", "10"])
            print("PC wird herhuntergefahren")
            print("'!' zum abbrechen")
            found = True
        elif "neustarten" in text:
            subprocess.run(["shutdown", "/r", "/t", "10"])
            print("PC wird neu gestartet")
            print("'!' zum abbrechen")
            found = True
        elif "benutzer abmelden" in text:
            subprocess.run(["shutdown", "/l"])
            print("Benutzer wurde abgemeldet")
            found = True
        elif "ruhezustand" in text:
            subprocess.run(["shutdown", "/h"])
            print("PC in Ruhezustand versetzt")
            found = True


    if "anhalten" in text or "pause" in text or "weiter" in text:
        pyautogui.press("playpause")
        found = True

    if "nächstes" in text or "überspringen" in text:
        pyautogui.press("next track")
        found = True

    if "zurück" in text:
        pyautogui.press("previous track")
        found = True

    if "musik aus" in text:
        keyboard.send("stop media")
        found = True

    if "einfügen" in text:
        keyboard.send("ctrl+v")
        found = True

    if "einstellungen" in text: #Einstellungen
        found = True
        print("Schnelleinstellungsmöglichkeiten:"
        "Eingabemodus: Sprache | Terminal"
        ""
        "-> Um die Einstellungen zu ändern, sage einfach die Einstellungskategurie und die Einstellungsmöglichkeit die du auswählen willst."
        ""
        "Warte auf Antwort... Um das Mnü zu verlassen, sage einfach >Beenden.<")

        if "beenden" in text:
            print("Einstellung geschlossen")
            return
        
    if text.startswith("?") or "Was kannst du?" in text or "Hilfe" in text: #Hilfe
        found = True
        print("Ich kann mehr als du!")
        print("Hier sind alle meine Befehle und Funktionen:")
        print("")
        funktionen = {
            "Transkripieren": "Sag einfach: 'Schreibe ...'",
            "Gamingmodus öffnen": "'Gamingmodus'",
            "Bestimmtes Programm öffnen": "Name des Programms",
            "PC Befehle: herunterfahren, neustarten, Benutzer abmelden, Ruhezustand": "'PC ...'",
            "Abbrechen (funktioniert nur bei bestimmten Befehlen)": "'!' oder 'Abbrechen' oder 'Stopp'",
            "Einstellungen": "'Einstellungen'",
            "Hilfeinformation / Befehlsübersicht": "'?' oder 'Was kannst du?' oder 'Hilfe'",
            "Zu erledingende ToDos ausgeben": "'ToDo'",
            "Erledigte ToDos ausgeben": "'Erledigte ToDos",
            "Alle ToDos ausgeben": "'alle ToDos'"
        }
        for keyword, funktions_beschreibung in funktionen.items():
            print(keyword, ":", funktions_beschreibung)
        
    if "todo" in text.replace(" ", "").replace("-", ""): #ToDo
        found = True
        settings = import_settings("data" / "todo.json")
        alle_aufgaben = settings[0]

        if "erledigt" in text:
            print("Hier sind alle erledigten ToDos:", end="\n\n")
            for nummer, details in alle_aufgaben.items():
                if details.get("Status") == "Erledigt":
                    if "debug" in text:
                        print(f"Debuginfo (interne Nummer): {nummer}")
                    print(f"{details["Aufgabe"]} ({details["Status"]})")
                    print(f"{details["Text"]}")
                    print("")

        elif "alle" in text:
            print("Hier sind alle ToDos:", end="\n\n")
            for nummer, details in alle_aufgaben.items():
                if "debug" in text:
                    print(f"Debuginfo (interne Nummer): {nummer}")
                print(f"{details["Aufgabe"]} ({details["Status"]})")
                print(f"{details["Text"]}")
                print("")

        else:
            print("Hier sind alle zu erledigenden ToDos:", end="\n\n")
            for nummer, details in alle_aufgaben.items():
                if details.get("Status") == "Nicht erledigt":
                    if "debug" in text:
                        print(f"Debuginfo (interne Nummer): {nummer}")
                    print(f"{details["Aufgabe"]} ({details["Status"]})")
                    print(f"{details["Text"]}")
                    print("")

    if "drücke" in text:
        befehl_zu_bestimmter_tastendruck(text)

    if "feuere ein laserstrahl" in text or "feuere ein laser-strahl" in text:
        os.startfile("laser_soundeffect.mp3")
        found = True
        
    if "!" == text or "abbrechen" in text or "stopp" in text:
        subprocess.run(["shutdown", "/a"])
        print("Aktion abgebrochen (Funktioniert nur bei bestimmten Befehlen)")
        found = True

    if not found:
        print("❌ Kein passender Befehl gefunden")
        return