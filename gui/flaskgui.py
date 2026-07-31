from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

#Dokument selbstgeschrieben


BASE_DIR = Path(__file__).parent.parent
SETTINGS = BASE_DIR / "data" / "settings.json"
with open(SETTINGS, "r") as file:
    settings = json.load(file)



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        eingabemodus_neu = request.form["eingabemodus_neu"]
        print(eingabemodus_neu)

        settings["eingabemodus"] = eingabemodus_neu
        with open(SETTINGS, "w") as file:
            json.dump(settings, file, indent=4)

    return render_template("index.html")


@app.route("/einstellungen", methods=["GET", "POST"])
def einstellungen():

    DATEI = Path(__file__).parent.parent / "data" / "settings.json"
    with open (DATEI, "r", encoding="utf-8") as f:
        daten = json.load(f)
    preference_triggerkey = daten["triggerkey"]

    if request.method == "POST":
        with open(SETTINGS, "r") as file:
            settings = json.load(file)

        triggerkey_neu = request.form["push to talk triggerkey"]
        print(triggerkey_neu)

        settings["triggerkey"] = triggerkey_neu
        with open(SETTINGS, "w") as file:
            json.dump(settings, file, indent=4)

    return render_template("einstellungen.html", preference_triggerkey = preference_triggerkey)


@app.route("/health")
def health():
    return jsonify({"message": "Hello world! I'm the web UI of the Jarvis System.", "app": "Charvis Web UI", "status": "running", "author": "Mael"})


if __name__ == "__main__":
    app.run(debug=True)