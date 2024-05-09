#1.booking,2.check pnr station,3.cancel,4.ticket download

import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator

def record_audio(duration, filename):
    # Record audio
    fs = 44100  # Sampling frequency
    print("starting........")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save audio to file
    wavio.write(filename, recording, fs, sampwidth=2)

def many_to_english(audio_file_path,language_input):
    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        print("Translating...")
        text = recognizer.recognize_google(audio, language=language_input)
        print("Translating to English...")
        translation = translator.translate(text, src=language_input, dest='en')
        return (translation.text)

    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def speak(destination,text,language_input):

    tts = gtts.gTTS(text=text, lang=language_input)
    tts.save("E:/collegefinal/data/recording/"+destination)
    playsound.playsound("E:/collegefinal/data/recording/"+destination)

def speak_options(language_input):
    if (language_input!="en"):
        translator = Translator()
        translation = translator.translate("for ticket booking say book ticket", src="en", dest=language_input)
        speak("bookticket.mp3",translation.text,language_input)
        translation = translator.translate("for checking pnr say pnr", src="en", dest=language_input)
        speak("pnr.mp3",translation.text,language_input)
        translation = translator.translate("for ticket cancelling say cancel ticket", src="en", dest=language_input)
        speak("cancelticket.mp3",translation.text,language_input)
        translation = translator.translate("for downloading ticket say download ticket", src="en", dest=language_input)
        speak("downloadticket.mp3",translation.text,language_input)

    else:
        speak("bookticket.mp3","for ticket booking say book ticket",language_input)
        speak("pnr.mp3","for checking pnr say pnr",language_input)
        speak("cancelticket.mp3","for ticket cancelling say cancel ticket",language_input)
        speak("downloadticket.mp3","for downloading ticket say download ticket",language_input)
def receive_options(language_input):
  if (language_input!="en"):
    translator = Translator()
    translation = translator.translate("select option", src="en", dest=language_input)
    speak("selectedoption.mp3",translation.text,language_input)
    record_audio(4,"currentoption.wav")
    selected_option=many_to_english("currentoption.wav",language_input)
    return selected_option
  else:
    speak("selectedoption.mp3","select option",language_input)
    record_audio(4,"currentoption.wav")
    selected_option=many_to_english("currentoption.mp3",language_input)
    return selected_option



    # record_audio(4,"pdetname.wav")
    # name=many_to_english("pdetname.wav",language_input)
    # return name