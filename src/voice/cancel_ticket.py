import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator
from src.voice import ticketbook
import time
from Database import dbsetup
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


def speak(destination,text,language_input):

    tts = gtts.gTTS(text=text, lang=language_input)
    if os.path.exists("data/recording/"+destination):
        os.remove("data/recording/"+destination)
    tts.save("data/recording/"+destination)
    playsound.playsound("data/recording/"+destination)


def cancel_train(language_input):
    try:
        translator = Translator()
        sentence_spoken=translator.translate("Enter your Pnr of 10 digit", src="en",dest=language_input).text
        speak("pnr_announce.mp3",sentence_spoken,language_input)
        record_audio(15,"recieved_pnr.mp3")
        recieved_pnr=str(many_to_english("recieved_pnr.mp3",language_input)).replace(" ","")
        
        selected_data={}
        if(len(recieved_pnr)==10):
            try:
                dbobj_user=dbsetup.connecttrainusers()
                for i in dbobj_user.find({ "pnr": {"$exists": True, "$eq": recieved_pnr}}):
                    selected_data = i
                if(selected_data!={} and selected_data !=None and selected_data['ticket_status']=="True"):

                    dbobj_user.update_one({ "pnr": {"$exists": True, "$eq": recieved_pnr}, "ticket_status" : {"$eq" : "True"}}, {"$set":{"ticket_status":"False"}})
                elif(selected_data!={} and selected_data !=None and selected_data['ticket_status']=="False"):
                    speak("ticket_already_cancel.mp3",translator.translate("Ticket Already Canceled",src="en",dest=language_input).text,language_input)
                else:
                    speak("wrong_pnr_1.mp3",translator.translate("Wrong Pnr Entered Refresh",src="en",dest=language_input).text,language_input)

            except Exception as e:

                print("Error:", e)
        else:
            speak("wrong_pnr.mp3",translator.translate("Wrong Pnr Entered Refresh",src="en",dest=language_input).text,language_input)
    except Exception as err:
        print(err)
  