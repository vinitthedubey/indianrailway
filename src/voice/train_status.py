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
def extract_train_info(html):
    # Parse the HTML
    soup = html

    # Find the desired div
    desired_div = soup.find('div', class_='z87fvf')

    # Extract the text
    if desired_div:
        train_info = desired_div.text.strip()
        # Split the text to get train number and name
        # train_number, train_name =  train_info.split('O– ')
        strid="\xa0–"
        ans=""
        for i in train_info:
            if(i not in strid):
                ans+=i
        train_number,train_name=ans[0:5],ans[5:]
        return train_number.strip(), train_name.strip()
    else:
        return None,None

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


def train_status(train_no,language_input):
    # Initialize Chrome WebDriver
    try:
        driver = webdriver.Chrome()

    # Construct the search query
        query = f"{train_no} train running status"
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
    
        train_data=bs(train_html,"html.parser")
        train_number,train_name=extract_train_info(train_data)
        big_unit=train_data.find_all("div",{"class":"MSEMzb"})

        curr_date=""
        time_train=""
        current_location=""
        translator = Translator()
        if(language_input!="en"):
            
            for i in range(len(big_unit)):
                curr_date=(big_unit[i].find("div",class_="QxnTCb").span.text)
                ch=["th1BOc UQq0xd","th1BOc pmXDEf"]
                try:
                    time_train=(big_unit[i].find("div",class_=ch[0] ).text)
                except Exception as e:
                    print(e)
                    time_train=(big_unit[i].find("div",class_=ch[1] ).text)
                current_location=(big_unit[i].find("div",class_="Bm205b").text)
                spoken_string=translator.translate(f"On {curr_date} Train number {train_number} Train Name {train_name} is currently at {current_location} is {time_train}",src="en",dest=language_input).text

                speak("train_status_ann.mp3",spoken_string,language_input)
        else:
            
            for i in range(len(big_unit)):
                curr_date=(big_unit[i].find("div",class_="QxnTCb").span.text)
                ch=["th1BOc UQq0xd","th1BOc pmXDEf"]
                try:
                    time_train=(big_unit[i].find("div",class_=ch[0] ).text)
                except Exception as f:
                    time_train=(big_unit[i].find("div",class_=ch[1] ).text)
                current_location=(big_unit[i].find("div",class_="Bm205b").text)
                spoken_string=(f"On {curr_date} Train number {train_number} Train Name {train_name} is currently at {current_location} is {time_train}")
                speak("train_status_ann.mp3",spoken_string,language_input)
    except Exception as f:
        speak("train_Status_error.mp3",translator.translate("Please enter correct Train Number",src="en",dest=language_input).text,language_input)
        

        





def receive_inputs_train_status(language_input):
    try:
        if(language_input!="en"):
            translator = Translator()
            translation = translator.translate("Say Train Number", src="en", dest=language_input)
            speak("train_number.mp3",translation.text,language_input)
            record_audio(6,"train_number_datarecieved.wav")
            train_number_status=many_to_english("train_number_datarecieved.wav",language_input)
            if(train_number_status!="" and train_number_status!=None):

                train_status(train_number_status,language_input)
            else:
                speak("wrong_train_number_status.mp3",translator.translate("No input Kindly Refresh",src="en",dest=language_input).text,language_input)
        else:
            speak("train_number.mp3","Say Train Number",language_input)
            record_audio(6,"train_number_datarecieved.wav")
            train_number_status=many_to_english("train_number_datarecieved.wav",language_input)
            if(train_number_status!="" and train_number_status!=None):

                train_status(train_number_status,language_input)
            else:
                speak("wrong_train_number_status.mp3","No input Kindly Refresh",language_input)
    except Exception as err:
        speak("wrong_train_number_status.mp3",translator.translate("Error Kindly Refresh",src="en",dest=language_input).text,language_input)
        print(err)
