# flask_gui.py

from core import handle_command, record_audio, transcribe_audio
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")

app_state = {
    "status": "Bereit",
    "last_command": "",
    "last_response": "",
    "last_transcript": "",
}

@app.route("/")
def index():
    return render_template("index.html", **app_state)

@app.route("/api/command", methods=["POST"])
def api_command():
    data = request.get_json(silent=True) or {}
    command = data.get("command", "").strip()
    if not command:
        return jsonify({"success": False, "message": "Bitte einen Befehl eingeben"}), 400

    app_state["status"] = "Befehl wird verarbeitet..."
    app_state["last_command"] = command

    result = handle_command(command)
    app_state["last_response"] = result["message"]
    app_state["status"] = "Bereit"
    return jsonify(result)

@app.route("/api/stt", methods=["POST"])
def api_stt():
    app_state["status"] = "Spracheingabe aufzeichnen..."
    audio = record_audio()
    if audio is None:
        app_state["last_response"] = "Keine Audioaufnahme erkannt."
        app_state["status"] = "Bereit"
        return jsonify({"success": False, "message": "Keine Audioaufnahme erkannt."})

    app_state["status"] = "Sprache wird transkribiert..."
    transcript = transcribe_audio(audio)
    app_state["last_transcript"] = transcript
    app_state["last_command"] = transcript

    result = handle_command(transcript)
    app_state["last_response"] = result["message"]
    app_state["status"] = "Bereit"
    return jsonify({
        "success": result["success"],
        "message": result["message"],
        "transcript": transcript,
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)