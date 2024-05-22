
from src import language_detection
from src import controller
from src.Passanger_details_in_voice import passanger_details_input
from src.voice import menu

from src.voice import ticketbook
from src.voice import train_status
from src.voice import cancel_ticket
from src.voice import download_ticket

#lang=language_detection.Run()

#lang_code=controller.controller(lang)

# print(menu.speak_options(lang_code))
# print(menu.speak_options(lang_code))
# print(test.gender(lang_code))
# print(menu.speak_options(lang_code))

# menu.speak_options(lang_code)
# print(menu.receive_options(lang_code))

# ticketbook.receive_inputs("en")

# train_status.receive_inputs_train_status("hi")

#ticketbook.receive_inputs_ticket_book("hi")

#download_ticket.recieve_input_download("hi")
# cancel_ticket.cancel_train("en")
# download_ticket.recieve_input_download("en")
#9892246557
#2855571061

# train_status.receive_inputs_train_status("en")

#ticketbook.receive_inputs_ticket_book("en")

#------------------------------------------------------------------------




import os
from flask import Flask, render_template, request,redirect
import playsound
import sounddevice as sd
import wavio
import gtts
import speech_recognition as sr
from googletrans import Translator
import random
from src.voice import menu

selected_global_language=""
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


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("homepage.html")
    elif request.method=="POST" and 'microphone-button' in request.form:
        count=0
        speak("greeting_welcome.mp3", "Welcome To Indian Railways", "en")
        lang_code=""
        while(count<=2 and lang_code==""):
            count+=1
            lang=language_detection.Run()
            lang_code=controller.controller(lang)
            global selected_global_language
            selected_global_language=lang_code
            print(lang_code)
            if(lang_code==""):
                speak("error_lanaguage.mp3","Please pronounce correctly","en")
        if(lang_code==""):
            speak("error_trial.mp3","trial limit exceded","en")
            return redirect('thanks.html')
        else:
            translator=Translator()
            speak("service_selection_option.mp3",translator.translate("do you want to use chatbot say chatbot",src="en",dest=lang_code).text,lang_code)
            record_audio(3,"service_selection_option_selected.mp3")
            service=many_to_english("service_selection_option_selected.mp3",lang_code)

            if service ==None or service=="":

                return redirect("/voiceservice.html")
            elif (service.upper().strip() in ["CHAT","BOT","CHAT BOT","CHATBOT","BOTCHAT","BOT CHAT","YES"]):
                return redirect('/index.html')
            else:
                return redirect("/voiceservice.html")
    else:
        return redirect('thanks.html')


@app.route('/voiceservice.html',methods=['GET', 'POST'])
def voiceservice():
    if request.method == 'GET':
        return render_template("voiceservice.html")
    elif request.method == 'POST' or 'background-image' in request.form:
        result=menu.receive_options(selected_global_language)
        if(result=="done"):
            return redirect('/thanks.html')
        else:
            return redirect('/thanks.html')
    else:
        return redirect('/thanks.html')

@app.route('/thanks.html',methods=["GET"])
def thanks():
    return render_template("thanks.html")



if __name__ == "__main__":
    app.run(debug=True)
