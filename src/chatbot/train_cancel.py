from googletrans import Translator
from src.voice import ticketbook
import time
from Database import dbsetup
import os

def cancel_train(recieved_pnr,language_input):
    try:
        translator = Translator()
        
        
        selected_data={}
        if(len(recieved_pnr)==10):
            try:
                dbobj_user=dbsetup.connecttrainusers()
                for i in dbobj_user.find({ "pnr": {"$exists": True, "$eq": recieved_pnr}}):
                    selected_data = i
                if(selected_data!={} and selected_data !=None and selected_data['ticket_status']=="True" and type(selected_data)==type({})):

                    dbobj_user.update_one({ "pnr": {"$exists": True, "$eq": recieved_pnr}, "ticket_status" : {"$eq" : "True"}}, {"$set":{"ticket_status":"False"}})
                    return (translator.tranlate("Ticket Cancelled Succesfully",src="en",dest=language_input).text)
                elif(selected_data!={} and selected_data !=None and selected_data['ticket_status']=="False" and type(selected_data)==type({})):
                    return(translator.translate("Ticket Already Canceled",src="en",dest=language_input).text)
                else:
                    return(translator.translate("Wrong Pnr Entered Refresh",src="en",dest=language_input).text)

            except Exception as e:

                print("Error:", e)
        else:
            return(translator.translate("Wrong Pnr Entered Refresh",src="en",dest=language_input).text)
    except Exception as err:
        print(err)
  