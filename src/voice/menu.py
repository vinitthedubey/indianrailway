import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator
from src.voice import ticketbook
import time
import os

from src.voice import train_status
from src.voice import download_ticket
from src.voice import cancel_ticket



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


def speak_options(language_input):
    if (language_input!="en"):
        translator = Translator()
        translation = translator.translate("for ticket booking say book ticket", src="en", dest=language_input)
        speak("bookticket.mp3",translation.text,language_input)
        translation = translator.translate("for checking train status say train status", src="en", dest=language_input)
        speak("pnr.mp3",translation.text,language_input)
        translation = translator.translate("for ticket cancelling say cancel ticket", src="en", dest=language_input)
        speak("cancelticket.mp3",translation.text,language_input)
        translation = translator.translate("for downloading ticket say download ticket", src="en", dest=language_input)
        speak("downloadticket.mp3",translation.text,language_input)
        translation=translator.translate("For Exit say Exit",src="en",dest=language_input)
        speak("exitoption.mp3",translation.text,language_input)

    else:
        speak("bookticket.mp3","for ticket booking say book ticket",language_input)
        speak("pnr.mp3","for checking train status say train status",language_input)
        speak("cancelticket.mp3","for ticket cancelling say cancel ticket",language_input)
        speak("downloadticket.mp3","for downloading ticket say download ticket",language_input)
        speak("exitoption.mp3","For Exit say Exit",language_input)


def receive_options(language_input):
  try:

    if (language_input!="en"):
        translator = Translator()
        speak_options(language_input)
        translation = translator.translate("select option", src="en", dest=language_input)
        speak("selectedoption.mp3",translation.text,language_input)
        record_audio(4,"currentoption.mp3")
        selected_option=many_to_english("currentoption.mp3",language_input)
        if(selected_option!="" and selected_option!=None):
            if (selected_option.upper().strip() in ["BOOK","BOOK TICKET","BOOKTICKET","TICKET","TICKETBOOK","TICKET BOOK","BOOK TRAIN","BOOKTRAIN","TRAIN BOOK","TRAINBOOK"]):
                ticketbook.receive_inputs_ticket_book(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["TRAIN STATUS","TRAINSTATUS","STATUS","STATUS TRAIN","STATUSTRAIN","TRAIN","TRAINCHECK","TRAIN CHECK","CHECK TRAIN","CHECKTRAIN"]):
                train_status.receive_inputs_train_status(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["CANCEL","TICKETCANCEL","TICKET CANCEL","CANCELLING TICKET","CANCELLINGTICKET","CANCEL TICKET","CANCELTICKET","CANCEL TRAIN","CANCELTRAIN","TRAIN CANCEL","TRAINCANCEL"]):
                cancel_ticket.cancel_train(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["DOWNLOAD","DOWNLOAD TICKET","DOWNLOADTICKET","TICKET DOWNLOAD","TICKETDOWNLOAD","DOWNLOADING"]):
                download_ticket.recieve_input_download(language_input)
                return "done"
            else:
                speak("MENUNOTSELECT.mp3",translator.translate("GOODBYE visit again",src="en",dest=language_input).text,language_input)
                return "done"
        else:
            speak("MENUNOTSELECT.mp3",translator.translate("GOODBYE visit again",src="en",dest=language_input).text,language_input)
            return "done"


    else:
        speak_options(language_input)
        speak("selectedoption.mp3","select option",language_input)
        record_audio(4,"currentoption.mp3")
        selected_option=many_to_english("currentoption.mp3",language_input)
        if(selected_option!="" and selected_option!=None):
            if (selected_option.upper().strip() in ["BOOK","BOOK TICKET","BOOKTICKET","TICKET","TICKETBOOK","TICKET BOOK","BOOK TRAIN","BOOKTRAIN","TRAIN BOOK","TRAINBOOK"]):
                ticketbook.receive_inputs_ticket_book(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["TRAIN STATUS","TRAINSTATUS","STATUS","STATUS TRAIN","STATUSTRAIN","TRAIN","TRAINCHECK","TRAIN CHECK","CHECK TRAIN","CHECKTRAIN"]):
                train_status.receive_inputs_train_status(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["CANCEL","TICKETCANCEL","TICKET CANCEL","CANCELLING TICKET","CANCELLINGTICKET","CANCEL TICKET","CANCELTICKET","CANCEL TRAIN","CANCELTRAIN","TRAIN CANCEL","TRAINCANCEL"]):
                cancel_ticket.cancel_train(language_input)
                return "done"
            elif(selected_option.upper().strip() in ["DOWNLOAD","DOWNLOAD TICKET","DOWNLOADTICKET","TICKET DOWNLOAD","TICKETDOWNLOAD","DOWNLOADING"]):
                download_ticket.recieve_input_download(language_input)
                return "done"
            else:
                speak("MENUNOTSELECT.mp3","GOODBYE visit again",language_input)
                return "done"
        else:
            speak("MENUNOTSELECT.mp3",("GOODBYE visit again"),language_input)
            return "done"
  except Exception as err:
      print(err)
      return "done"


