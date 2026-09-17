#Soll später als importierte funktion in core.py aufgerufen werden
#Modul zum einfach per (Sprach-)Befehle Tasten drücken
#Z.B. "Drücke Pfeiltaste rechts" -> rechte Pfeiltaste wird gedrückt

#Jahahahuiyy!!!



import keyboard

KEYS = {
        "recht": "nach-rechts",
        "link": "nach-links",
        "oben": "nach-oben",
        "unten": "nach-unten",
        "enter": "enter",
        "leer": "space"
    }

def befehl_zu_bestimmter_tastendruck(text):
    for key, name in KEYS.items():
        if key in text:
            keyboard.press_and_release(name)
            return True
        
    print("Diese Taste kenne ich noch nicht")
    return False

def what_a_key_is_this():
#utils oder so
    taste = keyboard.read_key()
    print(f"Gedrückte Taste {taste}")

def tastennamen_herausfinden():
    while True:
        what_a_key_is_this()