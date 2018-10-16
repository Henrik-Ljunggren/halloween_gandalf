#python3 -m pip install --user SpeechRecognition

import speech_recognition as sr

r = sr.Recognizer()

wav_file = sr.AudioFile("durin.wav")
with wav_file as source:
    audio = r.record(source)
    print(audio)
    print(r.recognize_sphinx(audio))
