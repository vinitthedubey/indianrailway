
from googletrans import Translator
import time
from Database import dbsetup
import os
from src import pdfmaking


def download_ticket(pnr,language_input):
    translator = Translator()
    selected_data={}
    if(len(pnr)==10):
      try:
        dbobj_user=dbsetup.connecttrainusers()
        selected_data = dbobj_user.find({ "pnr": {"$exists": True, "$eq": pnr}})
        
        
        for i in selected_data:
            selected_data=i

        if(selected_data!={} and  selected_data !=None):
            pdfmaking.generate_ticket(selected_data, "data/ticketpdf/indian_railway_ticket.pdf")
            return(translator.translate("Ticket downloaded",src="en",dest=language_input).text)
        else:
            return (translator.translate("No such Pnr Exist",src="en",dest=language_input).text)
        

          
      except Exception as e:

        print("Error:", e)
    



