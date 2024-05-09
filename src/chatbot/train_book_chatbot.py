from googletrans import Translator
import time
import random
from Database import dbsetup



def train_booking(train_details,passanger_detail,other_detail,language_input):
    try:
        translator=Translator()
        if(len(train_details)!=5):
            return (translator.translate("Error while accessing train details Refresh",src="en",dest=language_input).text)
    
        if(passanger_detail[0]!="" or (passanger_detail[1]=="" and translator.translate(passanger_detail[1],src=language_input,dest="en").text.isalnum()) or passanger_detail[2]=="" or passanger_detail[3]==""):
            return (translator.translate("Error while obtaining passanger details Refresh",src="en",dest=language_input).text)
        
        if(other_detail[0]=="" or other_detail[0]==None or other_detail[1]=="" or other_detail[1]==None or other_detail[2]=="" or other_detail[2]==None):
            return(translator.translate("Error while obtaining class details",src="en",dest=language_input).text)
        
        try:
            pnr=(''.join(random.choices('123456789',k=1)+(random.choices('0123456789',k=9))))

            dbobj_train=dbsetup.connecttrain()
            dbobj_user=dbsetup.connecttrainusers()
#data.append([translator.translate(train_number,src="en",dest=language_input).text,translator.translate(train_name,src="en",dest=language_input).text,translator.translate(from_station_name,src="en",dest=language_input).text,translator.translate(to_station_name,src="en",dest=language_input).text,translator.translate(from_station_code,src="en",dest=language_input).text,translator.translate(to_station_code,src="en",dest=language_input).text,translator.translate(from_station_arrival_time,src="en",dest=language_input).text,translator.translate(to_station_arrival_time,src="en",dest=language_input).text,translator.translate(from_station_arrival_date,src="en",dest=language_input).text,translator.translate(to_station_arrival_date,src="en",dest=language_input).text
#,translator.translate(class_size,src="en",dest=language_input).text,translator.translate(index,src="en",dest=language_input).text,translator.translate(seat_store,src="en",dest=language_input).text])

            traindata={"train_number":translator.translate(train_details[0],src=language_input,dest="en").text,"train_name":translator.translate(train_details[1],src=language_input,dest="en").text,"from_station_name":translator.translate(train_details[2],src=language_input,dest="en").text,
                                    "from_station_code":translator.translate(train_details[4],src=language_input,dest="en").text,"to_station_name":translator.translate(train_details[3],src=language_input,dest="en").text,"to_station_code":translator.translate(train_details[5],src=language_input,dest="en").text,"from_station_arrival_time":translator.translate(train_details[6],src=language_input,dest="en").text,"to_station_arrival_time":translator.translate(train_details[7],src=language_input,dest="en").text,
                                    "from_station_arrival_date":translator.translate(train_details[8],src=language_input,dest="en").text,"to_station_arrival_date":translator.translate(train_details[9],src=language_input,dest="en").text}
            
            userdata={"train_number":translator.translate(train_details[0],src=language_input,dest="en").text,"train_name":translator.translate(train_details[1],src=language_input,dest="en").text,"from_station_name":translator.translate(train_details[2],src=language_input,dest="en").text,
                                    "from_station_code":translator.translate(train_details[4],src=language_input,dest="en").text,"to_station_name":translator.translate(train_details[3],src=language_input,dest="en").text,"to_station_code":translator.translate(train_details[5],src=language_input,dest="en").text,"from_station_arrival_time":translator.translate(train_details[6],src=language_input,dest="en").text,"to_station_arrival_time":translator.translate(train_details[7],src=language_input,dest="en").text,
                                    "from_station_arrival_date":translator.translate(train_details[8],src=language_input,dest="en").text,"to_station_arrival_date":translator.translate(train_details[9],src=language_input,dest="en").text,"name":translator.translate(passanger_detail[0],src=language_input,dest="en").text,"age":translator.translate(passanger_detail[1],src=language_input,dest="en").text,"gender":translator.translate(passanger_detail[2],src=language_input,dest="en").text,"nationality":translator.translate(passanger_detail[3],src=language_input,dest="en").text,"selected_class":translator.translate(other_detail[0],src=language_input,dest="en").text,"current_status":translator.translate(other_detail[1],src=language_input,dest="en").text,"fare":translator.translate(other_detail[2],src=language_input,dest="en").text,"pnr":pnr,"ticket_status":"True"}
            print("pnr=",pnr)    
            dbobj_train.insert_one(traindata)
            dbobj_user.insert_one(userdata)
            return (translator.translate(f"Ticket Booked Successfully with pnr {pnr}",src="en",dest=language_input).text)
        
        except Exception as e:
            print(e)
        pass
    except Exception as err:
        print(err)