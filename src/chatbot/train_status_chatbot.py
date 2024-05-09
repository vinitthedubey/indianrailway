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
        data=[len(big_unit),train_number,translator.translate(train_name,src="en",dest=language_input).text]
        
            
        for i in range(len(big_unit)):
            curr_date=(big_unit[i].find("div",class_="QxnTCb").span.text)
            ch=["th1BOc UQq0xd","th1BOc pmXDEf"]
            try:
                time_train=(big_unit[i].find("div",class_=ch[0] ).text)
            except Exception as e:
                print(e)
                time_train=(big_unit[i].find("div",class_=ch[1] ).text)
            current_location=(big_unit[i].find("div",class_="Bm205b").text)
            data.append([translator.translate(curr_date,src="en",dest=language_input).text,translator.translate(current_location,src="en",dest=language_input).text,translator.translate(time_train,src="en",dest=language_input).text])
        return data
    except Exception as err:
        print(err)
        

        





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
