from assets import import_settings

def output(response):
    output_config = import_settings()["output"]

    if output_config["terminal"] == True:
        print(response)
        print("------")
