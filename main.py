#-----Grundanweisungen-----

import subprocess
import threading
import queue
import time

import core
from input.speech import listen
from  assets import is_flask_running, import_settings
from shared import input_queue
from input.wakeword import listen_with_wakeword
from input.terminal import terminal_input


print("♾️    Charvis Ist Bereit!", end="\n\n")


settings = import_settings()
input_options = settings["input"]
if settings["autostart_flaskgui"] == True:
    flask_status = is_flask_running()
    if flask_status == "NOT_RUNNING":
        subprocess.Popen(["python", "gui/flaskgui.py"])
    elif flask_status == "OTHER_APP_RUNNING":
        print("Fehler bei automatischem UI Start")
        print("ACHTUNG: Port 5000 ist bereits besetzt, aber nicht von Charvis Web UI")
        print("Die Web UI kann nicht gestartet werden. Bitte schließe zuerst die andere App und versuche es dann nochmal.")
if input_options["speech"] == True:
    print("Halte NUMPAD-0 zum Sprechen...")

#-----Grundlogik-----

def process_input(text):
    core.handle_command(text)

speech_thread = None
wakeword_thread = None
terminal_thread = None

def get_input():
    global speech_thread
    global wakeword_thread
    global terminal_thread

    settings = import_settings()
    input_options = settings["input"]
    wakeword_enabled = settings["wakeword"]


    if input_options["speech"] == True:
        if speech_thread is None or not speech_thread.is_alive():
            speech_thread = threading.Thread(target=listen, daemon=True)
            speech_thread.start()

    if wakeword_enabled == True:
        if wakeword_thread is None or not wakeword_thread.is_alive():
            wakeword_thread = threading.Thread(target=listen_with_wakeword, daemon=True)
            wakeword_thread.start()

    if input_options["terminal"] == True:
        if terminal_thread is None or not terminal_thread.is_alive():
            terminal_thread = threading.Thread(target=terminal_input, daemon=True)
            terminal_thread.start()

def worker():
    while True:
        text = input_queue.get()
        if text is None:
            break
        response = process_input(text)
        input_queue.task_done()
        output = import_settings()["output"]

threading.Thread(target=worker, daemon=True).start()


time.sleep(1)
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")



while True:
    text = get_input()



#Japadapadu!