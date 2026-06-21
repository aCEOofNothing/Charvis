from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Flask läuft!</h1>"

if __name__ == "__main__":
    print("Starte Flask Server...")
    app.run(debug=True, port=5050)
