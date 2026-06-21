from flask import Flask, render_template
import json, os
import threading
import webview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_data_path(name):
    return os.path.join(BASE_DIR, "data", f"{name}.json")

def load_json(name):
    path = os.path.join("data", f"{name}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name, data):
    path = os.path.join("data", f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


kontakte = load_json("kontakte") #Kontakte laden


if __name__ == "__main__":
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route("/abcdefg")
    def abcdefg():
        return "Etwas anderes"
    
    # Flask im Hintergrund starten
    def run_flask():
        app.run(debug=False, host="127.0.0.1", port=5000, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # PyWebView Fenster öffnen
    webview.create_window('Charvis System', 'http://127.0.0.1:5000/', width=1200, height=800)
    webview.start()