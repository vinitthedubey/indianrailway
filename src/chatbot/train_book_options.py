from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import time


def booking_details(from_station,to_destination,date,language_input):
    translator=Translator()
    
    

    try:
        if(from_station=="" or from_station==None or to_destination=="" or to_destination==None or date=="" or date==None):
            return(translator.translate("Kindly refresh",src="en",dest=language_input).text)
        
        
        source=translator.translate(from_station,src=language_input,dest="en").text
        destination=translator.translate(to_destination,src=language_input,dest="en").text
        timeandmonth=translator.translate(date,src=language_input,dest="en").text
        
        driver = webdriver.Chrome()

        # Construct the search query
        
        query = f"train for from {source} to {destination} on {timeandmonth}"
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
        data=[total_train]
        
        for count in range(total_train):
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
            for j in range(class_size):

                class_name=str(class_available[j]["data-seatingclass"])
                book_status=str(class_available[j].findAll("div")[8].text)
                class_price=str(class_available[j].find("div",{"class":"jzLLvc"}).text)
                seat_store[index[j]]=[class_name,book_status,class_price]

            data.append([train_number,translator.translate(train_name,src="en",dest=language_input).text,translator.translate(from_station_name,src="en",dest=language_input).text,translator.translate(to_station_name,src="en",dest=language_input).text,translator.translate(from_station_code,src="en",dest=language_input).text,translator.translate(to_station_code,src="en",dest=language_input).text,from_station_arrival_time,to_station_arrival_time,translator.translate(from_station_arrival_date,src="en",dest=language_input).text,translator.translate(to_station_arrival_date,src="en",dest=language_input).text,class_size,index,seat_store])

        
        
        return data
    
    
    
    
    except Exception as err:
        print("err=",err)


