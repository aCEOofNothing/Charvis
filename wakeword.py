import openwakeword
from openwakeword.model import Model
import soundcard as sc
import numpy as np
import collections
import time
#import pyaudio 


openwakeword.utils.download_models()

model = Model(wakeword_models=["hey_mycroft"])

print("Modelle:", model.models)
print("Sag 'Hey Jarvis'...")

mic = sc.default_microphone()

audio_buffer = collections.deque(maxlen=int(16000 * 1.5))

with mic.recorder(samplerate=16000) as recorder:
    while True:
        data = recorder.record(numframes=8000)

        data = np.array(data).astype(np.float32) [:, 0]

        audio_buffer.extend(data)


        frame_count =+ 1
        
        print(len(audio_buffer))
        if len(audio_buffer) >= 16000 and frame_count % 3==0:
            audio_data = np.array(audio_buffer)

            prediction = model.predict(audio_data)

            score = prediction["hey_mycroft"]

            print(f"Score: {score:.4f}")
            if score > 0.3:
                print(f"Score: {score:.4f}")

            if score > 0.6:
                print(">>> LET'S GOOOO <<<")
                time.sleep(1)