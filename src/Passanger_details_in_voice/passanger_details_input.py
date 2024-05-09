import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator
import os


def record_audio(duration,filename):
    # Record audio
    fs = 44100  # Sampling frequency
    print("starting........")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save audio to file
    wavio.write("data/recording/"+filename, recording, fs, sampwidth=2)

def many_to_english(audio_file_path,language_input):
    recognizer = sr.Recognizer()
    translator = Translator()

    with sr.AudioFile("data/recording/"+audio_file_path) as source:
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


#name age gender nationality
def speak(destination,text,language_input):

    tts = gtts.gTTS(text=text, lang=language_input)
    if os.path.exists("data/recording/"+destination):
        os.remove("data/recording/"+destination)
    tts.save("data/recording/"+destination)
    playsound.playsound("data/recording/"+destination)

def name(language_input):
    if (language_input!="en"):
        translator = Translator()
        translation = translator.translate("Say Your Name", src="en", dest=language_input)
        speak("temp1.mp3",translation.text,language_input)
    else:
        speak("temp1.mp3","Say Your Name",language_input)

    record_audio(4,"pdetname.wav")
    name=many_to_english("pdetname.wav",language_input)
    return name

def age(language_input):
    if(language_input!="en"):

        translator = Translator()
        translation = translator.translate("Say Your age", src="en", dest=language_input)
        speak("temp2.mp3",translation.text,language_input)
    else:
        speak("temp2.mp3","Say Your age",language_input)
    record_audio(4,"pdetage.wav")
    age=many_to_english("pdetage.wav",language_input)
    return age


def gender(language_input):
    if(language_input!="en"):
        translator = Translator()
        translation = translator.translate("select Your gender from male,female,others", src="en", dest=language_input)
        speak("temp3.mp3",translation.text,language_input)
    else:
        speak("temp3.mp3","select Your gender from male,female,others",language_input)
    record_audio(4,"pdetgender.wav")
    gender=many_to_english("pdetgender.wav",language_input)
    return gender

def nationality(language_input):
    if(language_input!="en"):
        translator = Translator()
        translation = translator.translate("Say Your nationality", src="en", dest=language_input)
        speak("temp5.mp3",translation.text,language_input)
    else:
        speak("temp5.mp3","Say Your nationality",language_input)
    record_audio(4,"pdet_nation.wav")
    nation=many_to_english("pdet_nation.wav",language_input)
    return nation


