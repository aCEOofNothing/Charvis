def autogreeting():
    from assets import import_settings
    settings = import_settings()
    name = settings["user"]["username"]
    print(f"Willkommen {name}!")
    return