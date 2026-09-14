import requests

from assets import import_settings

def output(response):
    output_config = import_settings()["output"]

    if output_config["terminal"] == True:
        print(response)
        print("------")
    if output_config["flaskgui"] == True:
        requests.post(url="http://127.0.0.1:5000/output_api", json=response)
