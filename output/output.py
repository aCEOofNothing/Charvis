import requests

from assets import import_settings


# idee: fehler werden gespeichert bei einem zusätzlichen argument und alle zusammen ausgegeben bei einem anderen und die variable hier wird geleert. fehler = None

def output(response):
    output_config = import_settings()["output"]

    if output_config["terminal"] == True:
        print(response)
        print("------")
    if output_config["flaskgui"] == True:
        try: requests.post(url="http://127.0.0.1:5000/output_api", json=response)
        except: print("fehler: FlaskGUI läuft nicht")

def outputline(response):
    output_config = import_settings()["output"]

    if output_config["terminal"] == True:
        print(response)
    if output_config["flaskgui"] == True:
        try: requests.post(url="http://127.0.0.1:5000/output_api", json=response)
        except: print("fehler: FlaskGUI läuft nicht")