from flask import Flask
import webview
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flask in a Desktop App!</h1>"

def start_flask():
    print("Starte Flask Server...")
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    # Starte Flask in einem eigenen Thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True  # beendet sich mit dem Hauptprogramm
    flask_thread.start()

    # Starte das Desktop-Fenster
    webview.create_window("Meine App", "http://127.0.0.1:5000", debug=True)
