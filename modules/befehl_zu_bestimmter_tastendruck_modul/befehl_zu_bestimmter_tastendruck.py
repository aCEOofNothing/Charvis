#Soll später als importierte funktion in core.py aufgerufen werden
#Modul zum einfach per (Sprach-)Befehle Tasten drücken
#Z.B. "Drücke Pfeiltaste rechts" -> rechte Pfeiltaste wird gedrückt

#Jahahahuiyy!!!



import keyboard

KEYS = {
        "escape": "esc",
        "recht": "nach-rechts",
        "link": "nach-links",
        "oben": "nach-oben",
        "unten": "nach-unten",
        "enter": "enter",
        "leer": "space",
        "eins": "1",
        "zwei": "2",
        "drei": "3",
        "vier": "4",
        "fünf": "5",
        "sechs": "6",
        "sieben": "7",
        "acht": "8",
        "neun": "9",
        "null": "0",    
        "tab": "tab",
        "löschen": "backspace",
        "a": "a",
        "b": "b",
        "c": "c",
        "d": "d",
        "e": "e",
        "f": "f",
        "g": "g",
        "h": "h",
        "i": "i",
        "j": "j",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "o": "o",
        "p": "p",
        "q": "q",
        "r": "r",
        "s": "s",
        "t": "t",
        "u": "u",
        "v": "v",
        "w": "w",
        "x": "x",
        "y": "y",
        "z": "z",
        "komma": ",",
        "punkt-komma": ";",
        "punkt": ".",
        "doppelpunkt": ":",
        "bindestrich": "-",
        "unterstrich": "_",
        "hashtag": "#",
        "apostroph": "'",
        "plus": "+",
        "tilde": "~",
        "sternchen": "*",
        "ausrufezeichen": "!",
        "fragezeichen": "?",
        "at": "@"
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