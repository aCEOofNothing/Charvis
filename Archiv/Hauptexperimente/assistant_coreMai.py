def handle_command(text: str) -> dict:
    original = text.strip()
    text = original.lower().strip()

    if not text:
        return {"success": False, "message": "Kein Text erhalten"}

    for trigger in ["schreibe", "schreib", "tippe", "tip"]:
        if text.startswith(trigger):
            to_type = original[len(trigger):].strip(" ,.!?\n")
            if to_type:
                keyboard.write(to_type)
                return {"success": True, "message": f"Text getippt: {to_type}"}
            return {"success": False, "message": "Nichts zum Schreiben erkannt"}

    if any(word in text for word in ("gaming", "videospiel", "freizeit")):
        started = []
        for app_name in ["steam", "spotify", "cortex"]:
            if app_name in COMMANDS:
                path, args = COMMANDS[app_name]
                subprocess.Popen([path] + args)
                started.append(app_name)
        if started:
            return {"success": True, "message": "Gaming-Modus gestartet: " + ", ".join(started)}
        return {"success": False, "message": "Keine Gaming-Apps gefunden"}

    for keyword, (path, args) in COMMANDS.items():
        if keyword in text:
            subprocess.Popen([path] + args)
            return {"success": True, "message": f"{keyword} wird gestartet"}
    return {"success": False, "message": "Kein passender Befehl gefunden"}

def transcribe_audio(audio: np.ndarray) -> str:
    segments, info = model.transcribe(
        audio,
        language="de",
        initial_prompt=(
            "Spotify ist ein Wort. Du bist ein Sprachassistent. Du bekommst Befehle wie: "
            "Bitte öffne Firefox. Häufig vorkommende Wörter sind: Spotify, Firefox, öffne, privat, Browser."
        ),
    )
    return "".join(segment.text for segment in segments)

def record_audio() -> np.ndarray | None:
    audio_chunks = []
    with mic.recorder(samplerate=fs) as recorder:
        while keyboard.is_pressed("num 0"):
            audio_chunks.append(recorder.record(4096))
    if not audio_chunks:
        return None
    audio = np.concatenate(audio_chunks, axis=0)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    return audio.astype(np.float32)

def run_voice_loop() -> None:
    print("Halte NUMPAD-0 zum Sprechen...")
    while True:
        keyboard.wait("num 0")
        print("🎤 Aufnahme...")
        audio = record_audio()
        if audio is None:
            print("❌ Keine Audioaufnahme erkannt.")
            continue
        print("🧠 Erkenne Sprache...")
        text = transcribe_audio(audio)
        print("➡️", text)
        result = handle_command(text)
        print(result["message"])
        print("------")