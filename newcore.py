



#handler mit argumenten starten fehlt im parser

# "Abbrechen"-Funktion muss gefixt werden






#Das ist der neue core (noch nicht integriert), der nicht mehr mit aneinandergereiten if-Abfragen funktioniert, sondern mit einem Registery das von einem Depatcher ausgelesen wird.

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
import time

from modules.befehl_zu_bestimmter_tastendruck_modul.befehl_zu_bestimmter_tastendruck import befehl_zu_bestimmter_tastendruck
from assets import save_settings, import_settings, is_flask_running, save_data, import_data
from output.output import output, outputline


#------application dict------

pc_applications = {
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


#------command definations------

def say_hello():
    found = True
    output("Hallo Meister!")

def start_gaming_mode():
    output("🎮 Gamingmodus wird gestartet...")

def shortcut_playpause():
    pyautogui.press("playpause")

def shortcut_next_track():
    pyautogui.press("next track")

def shortcut_prev_track():
    pyautogui.press("previous track")

def shortcut_stop_media():
    keyboard.send("stop media")

def shortcut_paste():
    keyboard.send("ctrl+v")

def wakeword_settings():
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

def start_gaming_mode():

    gaming_apps = [
             "steam",
             "spotify",
             "cortex"
        ]

    for app in gaming_apps:
                 
        if app not in pc_applications:
                output(f"❌ {app} existiert nicht im commands-Dictionary")
                continue

        path, args = pc_applications[app]

        output(f"🚀 Starte {app}")
        subprocess.Popen([path] + args)

    return

def pc_shutdown():
    subprocess.run(["shutdown", "/s", "/t", "10"])
    output("PC wird herhuntergefahren")
    output("'!' zum abbrechen")

def pc_restart():
    subprocess.run(["shutdown", "/r", "/t", "10"])
    output("PC wird neu gestartet")
    output("'!' zum abbrechen")

def pc_abmelden():
    subprocess.run(["shutdown", "/l"])
    output("Benutzer wurde abgemeldet")

def pc_ruhezustand():
    subprocess.run(["shutdown", "/h"])
    output("PC in Ruhezustand versetzt")

def start_write_sth(orginal_text, trigger):
    output("⌨️ Tippe Text...")
    to_type = orginal_text[len(trigger):].strip().strip(",.?!")
    if to_type:
        keyboard.write(to_type)
        output("⌨️ Text getippt: " + to_type)
    else:
        output("⚠️ Nichts zum Schreiben erkannt")

def open_settings(text):
    output("Schnelleinstellungsmöglichkeiten:")
    output("Eingabemodus: Sprache | Terminal")
    output("")
    output("-> Um die Einstellungen zu ändern, sage einfach die Einstellungskategurie und die Einstellungsmöglichkeit die du auswählen willst.")
    output("")
    output("Warte auf Antwort... Um das Mnü zu verlassen, sage einfach >Beenden.<")

    if "beenden" in text:
        output("Einstellung geschlossen")
        return

def helpcommand():
        outputline("Ich kann mehr als du!")
        outputline("Hier sind alle meine Befehle und Funktionen:")
        outputline("")
        for command, data in bigbabacommandsregistry.items():
            triggers = ""
            for trigger in data.get("triggers"):
                triggers = triggers + " " + trigger

            description = data.get("description")
            try: building_output = command + " : " + description + " (Trigger:" + triggers + ")"
            except: building_output = command + " : " + "Fehler: mehr Informationen sind nicht vorhanden"
            outputline(building_output)
            outputline("-")

        output("fertig")

def todo_shit(text):
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

def drücke_taste(text):
        befehl_zu_bestimmter_tastendruck(text)

def open_the_gui():
        flask_status = is_flask_running()
        if flask_status == "OTHER_APP_RUNNING":
            output("ACHTUNG: Port 5000 ist bereits besetzt, aber nicht von Charvis Web UI")
            output("Die Web UI kann nicht gestartet werden. Bitte schließe zuerst die andere App und versuche es dann nochmal.")
        else:
            if flask_status == "NOT_RUNNING":
                subprocess.Popen(["python", "gui/flaskgui.py"])
                output("Flaskserver für Charvis Web UI wird gestartet")
                time.sleep(0.5)
            output("Oberfläche wird geöffnet")
            path_to_electron_js = os.path.join('gui', 'index.js')
            subprocess.Popen(["electron", path_to_electron_js], shell=True)
            webbrowser.open("http://127.0.0.1:5000", new=1)
            subprocess.Popen(["start", "", "firefox", "--new-window", "http://127.0.0.1:5000"], shell=True)

def settings_input(text):
        settings = import_settings()
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

def laserstrahl():
    os.startfile("./media/laser_soundeffect.mp3")
    found = True
    output("Laserstrahl wird abgefeuer!")

def stop():
    subprocess.run(["shutdown", "/a"])
    output("Aktion abgebrochen (Funktioniert nur bei bestimmten Befehlen)")
    found = True






#------commands registery-----

bigbabacommandsregistry = {
    "stop": {
        "ultimate_triggers": ["!"],
        "triggers": ["abbrechen", "stopp"],
        "handler": "stop",
        "description": ""
    },

    "write_sth": {
        "i_need_this": ["orginal_text", "used_trigger"],
        "triggers": ["schreibe", "schreib", "tippe", "tip"],
        "handler": "start_write_sth",
        "description": "Tippt in dem Textfeld des Cursors, das was gesagt wurde."
    },

    "gaming_mode": {
        "triggers": ["gaming", "videospiel", "freizeit"],
        "handler": "start_gaming_mode",
        "description": ""
    },

    "say_hello": {
        "triggers": ["hallo"],
        "handler": "say_hello",
        "description": None
    },

    "shortcut_playpause": {
        "triggers": ["anhalten", "pause", "weiter"],
        "handler": "shortcut_playpause",
        "description": ""
    },

    "shortcut_next_track": {
        "triggers": ["nächstes", "überspringen"],
        "handler": "shortcut_next_track",
        "description": ""
    },

    "shortcut_prev_track": {
        "triggers": ["zurück"],
        "handler": "shortcut_prev_track",
        "description": ""
    },

    "shortcut_paste": {
        "triggers": ["einfügen"],
        "handler": "shortcut_paste",
        "description": ""
    },

    "shortcut_stop_media": {
        "triggers": ["musik aus"],
        "handler": "shortcut_stop_media",
        "description": ""
    },

    "wakeword_settings": {
        "triggers": ["komandowort"],
        "handler": "wakeword_settings",
        "description": ""
    },

    "pc_shutdown": {
        "second_triggers": ["herunterfahren"],
        "triggers": ["pc"],
        "handler": "pc_shutdown",
        "description": ""
    },

    "pc_restart": {
        "second_triggers": ["neustarten"],
        "triggers": ["pc"],
        "handler": "pc_restart",
        "description": ""
    },

    "pc_abmelden": {
        "second_triggers": ["benutzer abmelden"],
        "triggers": ["pc"],
        "handler": "pc_abmelden",
        "description": ""
    },

    "pc_ruhezustand": {
        "second_triggers":["ruhezustand"],
        "triggers": ["pc"],
        "handler": "pc_ruhezustand",
        "description": ""
    },

    "open_settings": {
        "i_need_this": ["text"],
        "triggers": ["einstellungen"],
        "handler": "open_settings",
        "description": ""
    },

    "helpcommand": {
        "triggers": ["?", "was kannst du?", "hilfe"],
        "handler": "helpcommand",
        "description": ""
    },

    "todo_shit": {
        "i_need_this": ["text"],
        "triggers": ["todo", "to do", "to-do"],
        "handler": "todo_shit",
        "description": ""
    },

    "drücke_taste": {
        "i_need_this": ["text"],
        "triggers": ["drücke"],
        "handler": "drücke_taste",
        "description": ""
    },

    "open_the_gui": {
        "triggers": ["öffne die oberfläche"],
        "handler": "open_the_gui",
        "description": ""
    },

    "settings_input": {
        "i_need_this": ["text"],
        "triggers": ["eingabe"],
        "handler": "settings_input",
        "description": ""
    },

    "laserstrahl": {
        "triggers": ["feuere ein laserstrahl", "feuere ein laser-strahl"],
        "handler": "laserstrahl",
        "description": ""
    },
}




#------depatcher / intent classivication------

def understand_command(text: str):  
    orginal_text = text.strip()
    text = orginal_text.lower().strip()

    used_trigger = None
    global command_context
    command_context = {
    "used_trigger": used_trigger,
    "orginal_text": orginal_text,
    "text": text
    }

    if not text:
        output("fuck you")
        return("text do not exist")

#funktioniert give arguments?
    for command, data in bigbabacommandsregistry.items():
        if data.get("ultimate_triggers"):
            for ultimatetrigger in data.get("ultimate_triggers"):
                if text == ultimatetrigger:
                    used_trigger = {"ultimatetrigger": ultimatetrigger}
                    command_context ["used_trigger"] = used_trigger
                    handler = data["handler"]
                    handler = globals()[handler]
                    if data.get("i_need_this"):
                        required_args = data["i_need_this"]

                        if not all(arg in command_context for arg in required_args):
                            print(f"Fehler: Benötigte Argumente fehlen")
                            return(f"Benötigte Argumente fehlen")
                        
                        give_arguments = [command_context[arg] for arg in required_args]
                        handler(*give_arguments)
                        return(f"Befehl erkannt: Command-Dictionary (mit ultimate trigger und i need this): {command}")
                    handler()
                    return(f"Befehl erkannt: Command-Dictionary (mit ultimate trigger): {command}")

        for trigger in data.get("triggers", []):
            if trigger in text:
                if data.get("second_triggers"):
                    for second_trigger in data.get("second_triggers", []):
                        if second_trigger in text:
                            used_trigger = {"trigger": trigger, "second_trigger": second_trigger}
                            command_context["used_trigger"] = used_trigger
                            handler = data["handler"]
                            handler = globals()[handler]
                            if data.get("i_need_this"):
                                required_args = data["i_need_this"]

                                if not all(arg in command_context for arg in required_args):
                                    print(f"Fehler: Benötigte Argumente fehlen")
                                    return(f"Benötigte Argumente fehlen")
                                
                                give_arguments = [command_context[arg] for arg in required_args]
                                handler(*give_arguments)
                                return(f"Befehl erkannt: Command-Dictionary (mit second trigger und i need this): {command}")
                            handler()
                            return(f"Befehl erkannt: Command-Dictionary (mit second trigger): {command}")

                else:
                    used_trigger = {"trigger": trigger}
                    command_context["used_trigger"] = used_trigger
                    handler = data["handler"]
                    handler = globals()[handler]
                    if data.get("i_need_this"):
                        required_args = data["i_need_this"]

                        if not all(arg in command_context for arg in required_args):
                            print(f"Fehler: Benötigte Argumente fehlen")
                            return(f"Benötigte Argumente fehlen")
                        
                        give_arguments = [command_context[arg] for arg in required_args]
                        handler(*give_arguments)
                        return(f"Befehl erkannt: Command-Dictionary (standart mit i need this): {command}")
                    handler()
                    return(f"Befehl erkannt: Command-Dictionary (standart): {command}")

    for keyword, (path, args) in pc_applications.items(): #Einzel-Öffnen

        if keyword in text:
            if not path:
                print("Fehler: App Pfad fehlt im Dictionary")
                return("Fehler")

            output_keyword=keyword.title()
            output(f"🚀 {output_keyword} wird gestartet...")
            subprocess.Popen([path] + args)
            return(f"Befehl erkannt: Einzelöffner: {output_keyword}")

    output("❌ Kein passender Befehl gefunden")
    return("Nix statt none")



#testscript for scripts mainfunction
ergebnis = understand_command("schreibe hallo")
print(ergebnis)


#command registery testscript
#The holy big german TÜV-Amt?
def test_all_comments():
    name_fehlt = 0
    handler_ungülltig = 0
    vorhanden = 0
    insgesamt_geforderte_args = set()

    for command, data in bigbabacommandsregistry.items():
        if data.get("i_need_this"):
            insgesamt_geforderte_args.update(data.get("i_need_this"))

        handler_name = data.get("handler")

        if not isinstance(handler_name, str):
            print(f"Handler Name fehlt: {command}")
            name_fehlt += 1
            continue

        handler = globals().get(handler_name)
        if not callable(handler):
            print(f"Handler ungülltig: {command}")
            handler_ungülltig += 1
            continue

        print(f"Command vorhanden: {command}")
        vorhanden += 1

    getestet = name_fehlt + handler_ungülltig + vorhanden
    ergebnis = {"vorhanden": vorhanden, "getestet": getestet, "name fehlt": name_fehlt, "handler ungülltig": handler_ungülltig, "insgesammt geforderte args": insgesamt_geforderte_args, }
    print("---Test fertig. Zusammenfassung:")
    print(f"Fehler: Handler Name fehlt ({name_fehlt}), Handler ungülltig ({handler_ungülltig})")
    print(f"Commands erreichbar und vorhanden: ({vorhanden}) von {getestet} getesteten")
    print(f"alle geforderten Args: {insgesamt_geforderte_args} ({len(insgesamt_geforderte_args)})")
    return(ergebnis)


if __name__ == "__main__":
    test_all_comments()






#------Alte Befehle-Logik-----
#(gehört nicht zum neuen core, ist auch nicht die vollständige alte Logik - die ist noch in core.py)

def handle_command(text):

    #Sprech-Einfüg-Funktion
    for trigger in []: 
        if text.startswith(trigger):
            found = True

            return #teständerung



    #komandowort


    #gaming_mode
    if any(word in text for word in ()): #Gamingmodus
        found = True
        output("🎮 Gamingmodus wird gestartet...")

        gaming_apps = [
             "steam",
             "spotify",
             "cortex"
        ]

        for app in gaming_apps:
                 
            if app not in pc_applications:
                output(f"❌ {app} existiert nicht im commands-Dictionary")
                continue

            path, args = pc_applications[app]

            output(f"🚀 Starte {app}")
            subprocess.Popen([path] + args)

        return

    for keyword, (path, args) in pc_applications.items(): #Einzel-Öffnen

        if keyword in text:
            output_keyword=keyword.upper
            output(f"🚀 {output_keyword} wird gestartet...")
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

#gut
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

#    plugin_list = import_data("core_py_plugins/plugin-list.json")
#    for keyword, name in plugin_list:
#        if keyword in text:
#            import_path = "core_py_plugins." + name
#            from import_path import name
#            name(text)

#    def load_plugins():
#        plugin_list = import_data("core_py_plugins/plugin-list.json")
#        name = "befehl_zu_bestimmter_tastendruck"
#        import core_py_plugins
    
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
                time.sleep(0.5)
            output("Oberfläche wird geöffnet")
            path_to_electron_js = os.path.join('gui', 'index.js')
            subprocess.Popen(["electron", path_to_electron_js], shell=True)
            webbrowser.open("http://127.0.0.1:5000", new=1)
            subprocess.Popen(["start", "", "firefox", "--new-window", "http://127.0.0.1:5000"], shell=True)

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






    