





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
import webbrowser

from modules.befehl_zu_bestimmter_tastendruck_modul.befehl_zu_bestimmter_tastendruck import befehl_zu_bestimmter_tastendruck
from assets import save_settings, import_settings, is_flask_running, save_data, import_data
from output.output import output


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
        output("fuck you")

    found = False

    for trigger in ["schreibe", "schreib", "tippe", "tip"]: #Sprech-Einfüg-Funktion
        if text.startswith(trigger):
            found = True
            output("⌨️ Tippe Text...")
            to_type = orginal_text[len(trigger):].strip().strip(",.?!")
            if to_type:
                keyboard.write(to_type)
                output("⌨️ Text getippt: " + to_type)
            else:
                output("⚠️ Nichts zum Schreiben erkannt")
            return #teständerung

    if "hallo" in text: #Hallo sagen
        found = True
        output("Hallo Meister!")

    if "komandowort" in text:
        found = True
        wakeword = import_settings("data/settings.json")["wakeword"]
        output(wakeword)
        if wakeword == True:
            output("True")
            return
        elif wakeword == False:
            output("False")
            return
        else:
            output("Nix")
            return

    if any(word in text for word in ("gaming", "videospiel", "freizeit")): #Gamingmodus
        found = True
        output("🎮 Gamingmodus wird gestartet...")

        gaming_apps = [
             "steam",
             "spotify",
             "cortex"
        ]

        for app in gaming_apps:
                 
            if app not in commands:
                output(f"❌ {app} existiert nicht im commands-Dictionary")
                continue

            path, args = commands[app]

            output(f"🚀 Starte {app}")
            subprocess.Popen([path] + args)

        return

    for keyword, (path, args) in commands.items(): #Einzel-Öffnen

        if keyword in text:
            output(f"🚀 {keyword} wird gestartet...")
            subprocess.Popen([path] + args)
            found = True
            break

    #Kritische Systembefehle:
    if "pc" in text:
        if "herunterfahren" in text:
            subprocess.run(["shutdown", "/s", "/t", "10"])
            output("PC wird herhuntergefahren")
            output("'!' zum abbrechen")
            found = True
        elif "neustarten" in text:
            subprocess.run(["shutdown", "/r", "/t", "10"])
            output("PC wird neu gestartet")
            output("'!' zum abbrechen")
            found = True
        elif "benutzer abmelden" in text:
            subprocess.run(["shutdown", "/l"])
            output("Benutzer wurde abgemeldet")
            found = True
        elif "ruhezustand" in text:
            subprocess.run(["shutdown", "/h"])
            output("PC in Ruhezustand versetzt")
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
        output("Schnelleinstellungsmöglichkeiten:")
        output("Eingabemodus: Sprache | Terminal")
        output("")
        output("-> Um die Einstellungen zu ändern, sage einfach die Einstellungskategurie und die Einstellungsmöglichkeit die du auswählen willst.")
        output("")
        output("Warte auf Antwort... Um das Mnü zu verlassen, sage einfach >Beenden.<")

        if "beenden" in text:
            output("Einstellung geschlossen")
            return
        
    if text.startswith("?") or "Was kannst du?" in text or "Hilfe" in text: #Hilfe
        found = True
        output("Ich kann mehr als du!")
        output("Hier sind alle meine Befehle und Funktionen:")
        output("")
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
            output(keyword, ":", funktions_beschreibung)
        
    if "todo" in text.replace(" ", "").replace("-", ""): #ToDo
        found = True
        settings = import_data("data/todo.json")
        alle_aufgaben = settings[0]

        if "erledigt" in text:
            output('"Hier sind alle erledigten ToDos:", end="\n\n"')
            for nummer, details in alle_aufgaben.items():
                if details.get("Status") == "Erledigt":
                    if "debug" in text:
                        output(f"Debuginfo (interne Nummer): {nummer}")
                    output(f"{details["Aufgabe"]} ({details["Status"]})")
                    output(f"{details["Text"]}")
                    output("")

        elif "alle" in text:
            output("Hier sind alle ToDos:", end="\n\n")
            for nummer, details in alle_aufgaben.items():
                if "debug" in text:
                    output(f"Debuginfo (interne Nummer): {nummer}")
                output(f"{details["Aufgabe"]} ({details["Status"]})")
                output(f"{details["Text"]}")
                output("")

        else:
            output("Hier sind alle zu erledigenden ToDos:", end="\n\n")
            for nummer, details in alle_aufgaben.items():
                if details.get("Status") == "Nicht erledigt":
                    if "debug" in text:
                        output(f"Debuginfo (interne Nummer): {nummer}")
                    output(f"{details["Aufgabe"]} ({details["Status"]})")
                    output(f"{details["Text"]}")
                    output("")

    if "drücke" in text:
        found = True
        befehl_zu_bestimmter_tastendruck(text)

    if "öffne die oberfläche" in text:
        found = True
        flask_status = is_flask_running()
        if flask_status == "OTHER_APP_RUNNING":
            output("ACHTUNG: Port 5000 ist bereits besetzt, aber nicht von Charvis Web UI")
            output("Die Web UI kann nicht gestartet werden. Bitte schließe zuerst die andere App und versuche es dann nochmal.")
        else:
            if flask_status == "NOT_RUNNING":
                subprocess.Popen(["python", "gui/flaskgui.py"])
                output("Flaskserver für Charvis Web UI wird gestartet")
        
            output("Oberfläche wird geöffnet")
            webbrowser.open("http://127.0.0.1:5000", new=1)

    elif "eingabe" in text: #Inputeinstellungen ändern
        found = True
        if "sprach" in text and "terminal" in text:
            output("Zu Sprach- und Terminaleingabe gewechselt")
            output("Halte NUMPAD-0 zum Sprechen...")
            mode = "speech+terminal"
            settings["eingabemodus"] = mode
            save_settings(settings)

        elif "sprache" in text:
            output("Zu Spracheingabe gewechselt")
            output("Halte NUMPAD-0 zum Sprechen...")
            mode = "speech"
            settings["eingabemodus"] = mode
            save_settings(settings)

        elif "terminal" in text:
            output("Zu Terminaleingabe gewechselt")
            mode = "terminal"
            settings["eingabemodus"] = mode
            save_settings(settings)

        else:
            output("❌ Bitte gib an, welchen Eingabemodus du öffnen möchtest ('Sprache', 'Terminal' oder 'Sprache und Terminal')")

    if "feuere ein laserstrahl" in text or "feuere ein laser-strahl" in text:
        os.startfile("./media/laser_soundeffect.mp3")
        found = True
        output("Laserstrahl wird abgefeuer!")
        
    if "!" == text or "abbrechen" in text or "stopp" in text:
        subprocess.run(["shutdown", "/a"])
        output("Aktion abgebrochen (Funktioniert nur bei bestimmten Befehlen)")
        found = True

    if not found:
        output("❌ Kein passender Befehl gefunden")
        return("Nix statt none")