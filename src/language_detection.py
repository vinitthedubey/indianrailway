import os
from flask import Flask, render_template, request
import playsound
import sounddevice as sd
import wavio
import gtts
import speech_recognition as sr
from googletrans import Translator
import random

app = Flask(__name__)

def record_audio(duration, filename):
    # Record audio
    fs = 44100  # Sampling frequency
    print("starting........")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save audio to file
    wavio.write("data/recording/" + filename, recording, fs, sampwidth=2)

def many_to_english(audio_file_path, language_input):
    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.AudioFile("data/recording/" + audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        print("Translating...")
        text = recognizer.recognize_google(audio, language=language_input)
        print("Translating to English...")
        translation = translator.translate(text, src=language_input, dest='en')
        return translation.text

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def speak(destination, text, language_input):
    tts = gtts.gTTS(text=text, lang=language_input)
    if os.path.exists("data/recording/" + destination):
        os.remove("data/recording/" + destination)
    tts.save("data/recording/" + destination)
    playsound.playsound("data/recording/" + destination)







    


def Run():
    arr=["data/hindif_option.mp3","data/englishf_option.mp3","data/marathif_option.mp3","data/bengalif_option.mp3","data/russianf_option.mp3","data/spanishf_option.mp3","data/teluguf_option.mp3","data/tamilf_option.mp3"]

    for i in arr:
        playsound.playsound(i)


    # Ask user to select preferred language
    speak("selection_language.mp3","Select your preferred language.","en")
    

    # Record audio
    record_audio(3,"language_selected.mp3")

   
    text = many_to_english("language_selected.mp3","en")
    return text
