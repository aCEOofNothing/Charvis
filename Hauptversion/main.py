#-----Grundanweisungen-----

import json
from pathlib import Path


import core
import speech


#------Einstellungen importieren------
BASE_DIR = Path(__file__).parent
SETTINGS = BASE_DIR / "data" / "settings.json"
with open(SETTINGS, "r") as file:
    settings = json.load(file)



#-----Grundlogik-----

    print("♾️    Charvis Ist Bereit!", end="\n\n")
    print("Halte NUMPAD-0 zum Sprechen...")
while True:


    text=speech.listen()

    core.handle_command(text)
        
    print("------")




#Japadapadu!