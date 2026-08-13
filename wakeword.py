import openwakeword
from openwakeword.model import Model
import soundcard as sc


openwakeword.utils.download_models()

model = Model(wakeword_models=["hey_jarvis"])

print(model.models)

mic = sc.default_microphone()

with mic.recorder(samplerate=16000) as recorder:

    while True:
        audio = recorder.record(numframes=1280)
        print(audio.max(), audio.min())
        audio = audio[:, 0]
        
        prediction = model.predict(audio)

        if prediction["hey_jarvis"] > 0.1:
            print("Let'ssssssss Gooo!!!")

        print(prediction["hey_jarvis"])