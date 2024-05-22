import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator
import time
from Database import dbsetup
import os
from src import pdfmaking

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

def download_ticket(pnr,language_input):
    translator = Translator()
    selected_data={}
    if(len(pnr)==10):
      try:
        dbobj_user=dbsetup.connecttrainusers()
        selected_data = dbobj_user.find({ "pnr": {"$exists": True, "$eq": pnr}})
        
        
        for i in selected_data:
            selected_data=i

        if(selected_data!={} and  selected_data !=None and type(selected_data)==type({})):
            return selected_data
        else:
            return None

          
      except Exception as e:
        return None
        print("Error:", e)
    



def recieve_input_download(language_input):
    try:

        if(language_input!="en"):
            translator = Translator()
            speak("download_pnr_req.mp3",(translator.translate("say your pnr",src="en",dest=language_input).text),language_input)
            record_audio(10,"download_pnr_data.mp3")
            pnr_recieved=str(many_to_english("download_pnr_data.mp3",language_input)).replace(" ","")


            user_data=download_ticket(pnr_recieved,language_input)
            if user_data !=None and user_data!={}:
                pdfmaking.generate_ticket(user_data, "data/ticketpdf/indian_railway_ticket.pdf")
                speak("tickedownloaded.mp3",translator.translate("Ticket Downloaded",src="en",dest=language_input).text,language_input)
            else:
                speak("wrong_pnr2.mp3",translator.translate("Wrong Pnr Entered Refresh",src="en",dest=language_input).text,language_input)

        else:
            speak("download_pnr_req.mp3","say your pnr",language_input)
            record_audio(10,"download_pnr_data.mp3")
            pnr_recieved=str(many_to_english("download_pnr_data.mp3",language_input)).replace(" ","")
            user_data=download_ticket(pnr_recieved,language_input)
            if user_data !=None and user_data!={}:
                pdfmaking.generate_ticket(user_data, "data/ticketpdf/indian_railway_ticket.pdf")
                speak("tickedownloaded.mp3",("Ticket Downloaded"),language_input)
            else:
                speak("wrong_pnr2.mp3","Wrong Pnr Entered Refresh",language_input)
    except Exception as err:
        print(err)