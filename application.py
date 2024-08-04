
from src import language_detection
from src import controller
import os
from flask import Flask, render_template, request,redirect,jsonify
import playsound
import sounddevice as sd
import wavio
import gtts
import speech_recognition as sr
from googletrans import Translator
from src.voice import menu
from src.chatbot import train_book_chatbot
from src.chatbot import train_book_options
from src.chatbot import train_status_chatbot
from src.chatbot import train_cancel
from src.chatbot import download_ticket_chatbot

selected_global_language="hi" #by default
response_data_train=[]
select_train_n=None

application = Flask(__name__)
app=application


# List to store train details
traindetailsreceived = []
traindetailsselected=[]
user_deatils=[]
classselected=[]


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
            print('service=',service)

            if service ==None or service=="":

                return redirect("/voiceservice.html")
            elif (any(sub in ["CHAT", "BOT","CHAAT","BOAT", "CHAT BOT", "CHATBOT", "BOTCHAT", "BOT CHAT", "YES"] for sub in (service[i:j].upper().strip() for i in range(len(service)) for j in range(i + 1, len(service) + 1)))):
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

@app.route('/index.html',methods=['GET', 'POST'])
def cahtbotcall():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    translator=Translator()
    user_message = request.json.get('message')
    chat_state = request.json.get('state')
    
    
    if user_message:
        if user_message.lower() == 'exit':
            return jsonify({"redirect": True, "url": "/thanks.html"})
        
        if chat_state == 'init':
            if user_message == 'Book Ticket':
                return jsonify({"response": translator.translate("Please enter source station:",src="en",dest=selected_global_language).text, "state": "source"})
            elif user_message == 'Download Ticket':
                return jsonify({"response": translator.translate("Please enter PNR number:",src="en",dest=selected_global_language).text, "state": "pnr_download"})
            elif user_message == 'Cancel Ticket':
                return jsonify({"response": translator.translate("Please enter PNR number:",src="en",dest=selected_global_language).text, "state": "pnr_cancel"})
            elif user_message == 'Train Status':
                return jsonify({"response": translator.translate("Please enter train number:",src="en",dest=selected_global_language).text, "state": "train_status"})
            elif str(user_message).upper() in ["HI","HELLO","HEY","HOLA","GOODMORNING","GOOD MORNING","GOOD EVENING","GOODEVENING","GOODAFTERNOON","GOOD AFTERNOON","GOOD NIGHT","GOODNIGHT"]:
                return jsonify({"response": translator.translate("Welcome to Indian Railway chatbot!",src="en",dest=selected_global_language).text, "state": "init"})
            elif str(user_message).upper() in ["BYE","GOODBYE","GOOD BYE","THANKS","NICE","SEE YOU"]:
                return jsonify({"response": translator.translate("Thank for choosing Indian Railway chatbot!",src="en",dest=selected_global_language).text, "state": "init"})
            else:
                return jsonify({"response": translator.translate("Apologies, I'm not equipped with that information right now. Feel free to ask me about ticket bookings, Train status, or download ticket instead!",src="en",dest=selected_global_language).text, "state": "init"})
        elif chat_state == 'source':
            traindetailsreceived.append(user_message)
            return jsonify({"response": translator.translate("Please enter destination station:",src="en",dest=selected_global_language).text, "state": "destination"})
        elif chat_state == 'destination':
            traindetailsreceived.append (user_message)
            return jsonify({"response": translator.translate("Please enter date and month (DD-Month):",src="en",dest=selected_global_language).text, "state": "date"})
        elif chat_state == 'date':
            traindetailsreceived.append(user_message)
            return jsonify({"response": translator.translate("To Show Available Trains Press 1",src="en",dest=selected_global_language).text, "state": "display"})
        elif chat_state == 'display':
            z=user_message
            global response_data_train
            response_data_train=train_book_options.booking_details(traindetailsreceived[0],traindetailsreceived[1],traindetailsreceived[2],selected_global_language)
            if(response_data_train=="" or response_data_train==None or response_data_train==[]):
                return(jsonify({"response": translator.translate("Restart Error Ocurred!!",src="en",dest=selected_global_language).text, "state": "init"}))
            
            response_message=(
                f"<strong>Train Available:</strong> {response_data_train[0]}<br>"
                
            )
            t=response_data_train[0]

            for i in range(1,t+1):
                temp=translator.translate("To select this train enter",src="en",dest=selected_global_language).text
                
                response_message+=(
                    f"<strong> {temp} {i}</strong><br>"
                    f"Train number: {response_data_train[i][0]} <br> Train Name: {response_data_train[i][1]}<br>"
                    f"FROM : {response_data_train[i][2]}<br> ({response_data_train[i][4]})<br>"
                    f"Departurture time: {response_data_train[i][6]}<br> Date : {response_data_train[i][8]}"
                    f"TO : {response_data_train[i][3]}<br> ({response_data_train[i][5]})<br>"
                    f"Arrival time: {response_data_train[i][7]}<br> Date : {response_data_train[i][9]}<br>"
                )

                response_message+=(f"CLASS DETAILS<br>")

                for j in range(response_data_train[i][10]):
                    response_message+=(
                        f"{response_data_train[i][12][response_data_train[i][11][j]][0]} | {response_data_train[i][12][response_data_train[i][11][j]][1]} | {response_data_train[i][12][response_data_train[i][11][j]][2]} <br>"
                    )
                response_message+="<br><br>"
            response_message+="<br><strong>Select Train</strong>"


            return jsonify({"response": response_message, "state": "selectedtrain"})
        
        elif chat_state=='selectedtrain':
            global select_train_n
            select_train_n=int(user_message)
            traindetailsselected.append(response_data_train[select_train_n][0])
            traindetailsselected.append(response_data_train[select_train_n][1])
            traindetailsselected.append(response_data_train[select_train_n][2])
            traindetailsselected.append(response_data_train[select_train_n][3])
            traindetailsselected.append(response_data_train[select_train_n][4])
            traindetailsselected.append(response_data_train[select_train_n][5])
            traindetailsselected.append(response_data_train[select_train_n][6])
            traindetailsselected.append(response_data_train[select_train_n][7])
            traindetailsselected.append(response_data_train[select_train_n][8])
            traindetailsselected.append(response_data_train[select_train_n][9])

            response_message=(
                f"<strong>Train Class Available:</strong> {response_data_train[0]}<br>"
                
            )

            for j in range(response_data_train[select_train_n][10]):
                    temp=translator.translate("To select This class enter",src="en",dest=selected_global_language).text
                    response_message+=(
                        f"<strong>{temp} {j}</strong><br>"
                        f"{response_data_train[select_train_n][12][response_data_train[select_train_n][11][j]][0]} | {response_data_train[select_train_n][12][response_data_train[select_train_n][11][j]][1]} | {response_data_train[select_train_n][12][response_data_train[select_train_n][11][j]][2]} <br>"
                    )
            response_message+="<br><br>"
            response_message+="<br><strong>Select Class</strong>"

            return jsonify({"response": response_message, "state": "selectedclassn"})
        elif chat_state=='selectedclassn':
            select_train_class_n=int(user_message)

            classselected.append(response_data_train[select_train_n][12][response_data_train[select_train_n][11][select_train_class_n]][0])
            classselected.append(response_data_train[select_train_n][12][response_data_train[select_train_n][11][select_train_class_n]][1])
            classselected.append(response_data_train[select_train_n][12][response_data_train[select_train_n][11][select_train_class_n]][2])

            return jsonify({"response": translator.translate("Please Enter Your Name",src="en",dest=selected_global_language).text, "state": "name"})



        
        elif chat_state=='name':
            user_deatils.append(user_message)
            return jsonify({"response": translator.translate("Please Enter Your Age",src="en",dest=selected_global_language).text, "state": "age"})
        
        elif chat_state=='age':
            user_deatils.append(user_message)
            return jsonify({"response": translator.translate("Please Enter Your Gender",src="en",dest=selected_global_language).text, "state": "gender"})
        
        elif chat_state=='gender':
            user_deatils.append(user_message)
            return jsonify({"response": translator.translate("Please Enter Your Nationality",src="en",dest=selected_global_language).text, "state": "nationality"})
        elif chat_state=='nationality':
            user_deatils.append(user_message)
            response_message=train_book_chatbot.train_booking(traindetailsselected,user_deatils,classselected,selected_global_language)
            return jsonify({"response": response_message, "state": "init"})

             
        elif chat_state == 'pnr_download':
            pnr = user_message
            response_message = download_ticket_chatbot.download_ticket(pnr, selected_global_language)
            return jsonify({"response": response_message, "state": "init"})
        elif chat_state == 'pnr_cancel':
            pnr = user_message
            response_message = train_cancel.cancel_train(pnr,selected_global_language)
            return jsonify({"response": response_message, "state": "init"})
        elif chat_state == 'train_status':
            train_no = user_message
            response_data = train_status_chatbot.train_status(train_no, selected_global_language)
            response_message = (
                f"<strong>Train Number:</strong> {response_data['train_number']}<br>"
                f"<strong>Train Name:</strong> {response_data['train_name']}<br><br>"
                "<table border='1' style='border-collapse: collapse;'>"
                "<tr><th>Date</th><th>Location</th><th>Time</th></tr>"
            )
            for status in response_data['status']:
                response_message += (
                    f"<tr>"
                    f"<td>{status['date']}</td>"
                    f"<td>{status['location']}</td>"
                    f"<td>{status['time']}</td>"
                    f"</tr>"
                )
            response_message += "</table>"
            return jsonify({"response": response_message, "state": "init"})
    
    return jsonify({"response": translator.translate("I didn't understand that. Please try again.",src="en",dest=selected_global_language).text, "state": "init"})


@app.route('/thanks.html',methods=["GET"])
def thanks():
    return render_template("thanks.html")



if __name__ == "__main__":
    app.run(host="0.0.0.0")
