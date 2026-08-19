from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from assets import import_settings, save_settings

#Dokument selbstgeschrieben

settings = import_settings()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        input_options_changed = request.form.getlist("input_options_value")
        settings = import_settings()
        settings["input"]["speech"] = input_options_changed["speech"]
        settings["input"]["terminal"] = input_options_changed["terminal"]
        save_settings(settings)

    return render_template("index.html")


@app.route("/einstellungen", methods=["GET", "POST"])
def einstellungen():

    settings = import_settings()
    preference_triggerkey = settings["triggerkey"]

    if request.method == "POST":
        settings = import_settings()

        triggerkey_neu = request.form["push to talk triggerkey"]
        print(triggerkey_neu)

        settings["triggerkey"] = triggerkey_neu
        save_settings(settings)

    return render_template("einstellungen.html", preference_triggerkey = preference_triggerkey)


@app.route("/health")
def health():
    return jsonify({"message": "Hello world! I'm the web UI of the Jarvis System.", "app": "Charvis Web UI", "status": "running", "author": "Mael"})


if __name__ == "__main__":
    app.run(debug=True)