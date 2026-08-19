import openwakeword
from openwakeword.model import Model
import soundcard as sc
import numpy as np
import collections
import time

from assets import import_settings
from input.speech import short_listen


openwakeword.utils.download_models()

wakeword_word = import_settings()["wakeword_word"]
model = Model(wakeword_models=[wakeword_word])

print(f"Sage '{wakeword_word.replace("_", " ")}!'...")

mic = sc.default_microphone()

def wakeword():
    audio_buffer = collections.deque(maxlen=int(16000 * 1.5))

    frame_count = 0

    with mic.recorder(samplerate=16000) as recorder:
        while True:
            data = recorder.record(numframes=8000)

            data = np.array(data)

            if data.ndim == 2:
                data = data[:, 0]

            data = (data * 32767).astype(np.int16)

            audio_buffer.extend(data)


            frame_count += 1
            
            if len(audio_buffer) >= 16000 and frame_count % 3==0:
                audio_data = np.array(audio_buffer)

                prediction = model.predict(audio_data)

                score = prediction[wakeword_word]

                if score > 0.6:
                    print("Wakeword erkannt!")
                    return True

    return False

def listen_with_wakeword():
    if wakeword():
        short_listen(seconds=5)