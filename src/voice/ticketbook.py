import playsound
import sounddevice as sd
import wavio
import pyttsx3
import gtts
import speech_recognition as sr
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from src.voice import ticketbook
import time
from src.Passanger_details_in_voice import passanger_details_input
from Database import dbsetup
import os
import random

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










def train_details_book(from_station, to_station, date,language_input):
    try:

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome()

        # Construct the search query
        query = f"train for from {from_station} to {to_station} on {date}"
        google_url = f"https://www.google.com/search?q={query}"

        # Open Google Search
        driver.get(google_url)
        time.sleep(2)  # Wait for page to load

        # Get the page source
        page_source = driver.page_source

        # Close the WebDriver
        driver.quit()

        # Parse the HTML
        train_html = page_source
        
        train_page=bs(train_html,"html.parser")
        big_unit=train_page.find_all("div",{"class":"xFJoje"})
        total_train = len(big_unit)

        choice_train=""
        choice_more=""
        flag=0
        check_limit=0
        count=-1
        translator = Translator()

        while(choice_train.upper() not in ["BOOK","TICKET","BOOK TICKET","TICKET","BOOKTICKET","TICKETBOOK","TICKET BOOK","YES"] and flag !=1):
            

            for i in range(1,6):
                count+=1
                if(count>=total_train or flag==1):
                    break
                

                train_number=big_unit[count].div.div.text
                train_name=big_unit[count].div.span.text
                from_station_name=big_unit[count].findAll("span",{"class":"K5U9Jc"})[0].text
                to_station_name=big_unit[count].findAll("span",{"class":"K5U9Jc"})[1].text
                from_station_code=big_unit[count].find("div",{"class":"OaSFld"}).span.text
                to_station_code=big_unit[count].find("div",{"class":"GYynId"}).span.text
                from_station_arrival_time=big_unit[count].find("div",{"class":"xdhUo"}).span.text
                to_station_arrival_time=big_unit[count].find("div",{"class":"Rm1Xdc"}).span.text
                from_station_arrival_date=big_unit[count].find("span",{"class":"Ggd3ie"}).text
                to_station_arrival_date=big_unit[count].find("span",{"class":"ALe5qd"}).text
                #seat details
                class_available=big_unit[count].findAll("div",{"class":"cp2zCc yp"})
                class_size=len(class_available)
                index=["first","second","third","fourth","fivth","sixth","seventh","eighth","nineth","tenth"]
                seat_store={}
                


                #senetence to speak

                
                if (language_input!="en" or language_input=="en"):
                    
                    sentence_train_details=translator.translate(f"Train {train_number} ({train_name}) departs from {from_station_name} ({from_station_code}) at {from_station_arrival_time} on {from_station_arrival_date} and arrives at {to_station_name} ({to_station_code}) at {to_station_arrival_time} on {to_station_arrival_date}.",src="en",dest=language_input).text
                    speak("traindetail.mp3",sentence_train_details,language_input)
                    speak("seat_ann.mp3",translator.translate("Seating Availability are",src="en", dest=language_input).text,language_input)
                    for j in range(class_size):

                        class_name=str(class_available[j]["data-seatingclass"])
                        book_status=str(class_available[j].findAll("div")[8].text)
                        class_price=str(class_available[j].find("div",{"class":"jzLLvc"}).text)
                        seat_store[index[j]]=[class_name,book_status,class_price]
                        sentence_seat_details=(f"Class {class_name} current status {book_status} and price {class_price}")
                        speak("seat_details.mp3",translator.translate(sentence_seat_details,src="en", dest=language_input).text,language_input)
                    speak("choicetrain.mp3",translator.translate("do you want to book train ? Say ticket book",src="en", dest=language_input).text,language_input)
                    record_audio(3,"choice_train.mp3")
                    choice_train=many_to_english("choice_train.mp3",language_input)

                    if(choice_train!=None and choice_train.upper() in ["BOOK","TICKET","BOOK TICKET","TICKET","BOOKTICKET","TICKETBOOK","TICKET BOOK","YES"]):
                        speak("selectclass.mp3",translator.translate("select class",src="en", dest=language_input).text,language_input)
                        selected_class,current_status,fare="","",""
                        for k in seat_store:
                            sentence_option_class=translator.translate(f"To select {seat_store[k][0]} with current status {seat_store[k][1]} say {k}",src="en",dest=language_input).text
                            speak("seat.mp3",sentence_option_class,language_input)
                        record_audio(3,"selected_class.mp3")
                        try:
                            selected_class_t=many_to_english("selected_class.mp3",language_input)
                            if(selected_class_t!=None):
                                selected_class_t=selected_class_t.lower()
                            
                            if(selected_class_t in seat_store and selected_class_t !=None):
                                selected_class=seat_store[selected_class_t][0]
                                current_status=seat_store[selected_class_t][1]
                                fare=seat_store[selected_class_t][2]
                            else:
                                
                                speak("class_select.mp3",translator.translate("select the option again",src="en",dest=language_input).text,language_input)
                                record_audio(3,"selected_class.mp3")
                                selected_class_t=many_to_english("selected_class.mp3",language_input)
                                if(selected_class_t!=None):
                                    selected_class_t=selected_class_t.lower()

                                if(selected_class_t not in seat_store or selected_class_t==None):
                                    speak("final_try_class_select.mp3",translator.translate("Wrong Choice Limit Excedded Please refresh",src="en",dest=language_input).text,language_input)
                                    check_limit=1
                                    break
                                selected_class=seat_store[selected_class_t][0]
                                current_status=seat_store[selected_class_t][1]
                                fare=seat_store[selected_class_t][2]
                                
                        except Exception as e:
                            speak("class_select_error.mp3",translator.translate("Error Please Refresh",src="en",dest=language_input).text,language_input)
                            break
                            print(e)


                        name=passanger_details_input.name(language_input)
                        age=passanger_details_input.age(language_input)
                        gender=passanger_details_input.gender(language_input)
                        nationality=passanger_details_input.nationality(language_input)
                        pnr=(''.join(random.choices('123456789',k=1)+(random.choices('0123456789',k=9))))

                        dbobj_train=dbsetup.connecttrain()
                        dbobj_user=dbsetup.connecttrainusers()

                        traindata={"train_number":train_number,"train_name":train_name,"from_station_name":from_station_name,
                                    "from_station_code":from_station_code,"to_station_name":to_station_name,"to_station_code":to_station_code,"from_station_arrival_time":from_station_arrival_time,"to_station_arrival_time":to_station_arrival_time,
                                    "from_station_arrival_date":from_station_arrival_date,"to_station_arrival_date":to_station_arrival_date}
                        userdata={"train_number":train_number,"train_name":train_name,"from_station_name":from_station_name,
                                    "from_station_code":from_station_code,"to_station_name":to_station_name,"to_station_code":to_station_code,"from_station_arrival_time":from_station_arrival_time,"to_station_arrival_time":to_station_arrival_time,
                                    "from_station_arrival_date":from_station_arrival_date,"to_station_arrival_date":to_station_arrival_date,"name":name,"age":age,"gender":gender,"nationality":nationality,"selected_class":selected_class,"current_status":current_status,"fare":fare,"pnr":pnr,"ticket_status":"True"}
                        print("pnr=",pnr)    
                        dbobj_train.insert_one(traindata)
                        dbobj_user.insert_one(userdata)
                        flag=1
                        speak("goodbye.mp3",translator.translate(f"Ticket Booked Succesfully and pnr is {pnr}",src="en",dest=language_input).text,language_input)

                        
                    else:
                        pass





                
            
            if(check_limit==1):
                break
            
            if(flag!=1):
                speak("moretrain.mp3",translator.translate("Want More Train Say more",src="en",dest=language_input).text,language_input)
                record_audio(3,"moretrainchoice.mp3")
                choice_more=many_to_english("moretrainchoice.mp3",language_input)

            if(choice_more.upper() in ["MORE","MANY","NEXT","FURTHER","PROCEED"] and flag!=1):
                pass
            else:
                break 
    except Exception as err:
        speak("big_error.mp3",translator.translate("Error Please Refresh",src="en",dest=language_input).text,language_input)
        print(err)

                


            
            
def receive_inputs_ticket_book(language_input):
    try:
        if(language_input!="en"):
            translator = Translator()
            translation = translator.translate("Say source station", src="en", dest=language_input)
            speak("bookdatafrom.mp3",translation.text,language_input)
            record_audio(4,"bookdatarecieved_from.wav")
            data_received_fromstation=many_to_english("bookdatarecieved_from.wav",language_input)
            

            translation = translator.translate("Say destination station", src="en", dest=language_input)
            speak("bookdatadest.mp3",translation.text,language_input)
            record_audio(4,"bookdatarecieved_dest.wav")
            data_received_deststation=many_to_english("bookdatarecieved_dest.wav",language_input)

            translation = translator.translate("Say date", src="en", dest=language_input)
            speak("bookdatadate.mp3",translation.text,language_input)
            record_audio(4,"bookdatarecieved_date.wav")
            data_received_date=many_to_english("bookdatarecieved_date.wav",language_input)

            train_details_book( data_received_fromstation,data_received_deststation,data_received_date,language_input)
        else:
            speak("bookdatafrom.mp3","Say source station",language_input)
            record_audio(4,"bookdatarecieved_from.wav")
            data_received_fromstation=many_to_english("bookdatarecieved_from.wav",language_input)
            speak("bookdatadest.mp3","Say destination station",language_input)
            record_audio(4,"bookdatarecieved_dest.wav")
            data_received_deststation=many_to_english("bookdatarecieved_dest.wav",language_input)
            speak("bookdatadate.mp3","Say date",language_input)
            record_audio(4,"bookdatarecieved_date.wav")
            data_received_date=many_to_english("bookdatarecieved_date.wav",language_input)
            train_details_book( data_received_fromstation,data_received_deststation,data_received_date,language_input)
    except Exception as err:
        print(err)





        

        