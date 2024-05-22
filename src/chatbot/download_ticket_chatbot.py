import os,sys
from os.path import dirname,join,abspath


from googletrans import Translator
import time
sys.path.insert(0, abspath(join(dirname(__file__), '..', '..')))
from Database import dbsetup



from src import pdfmaking






def download_ticket(pnr,language_input):
    
    translator = Translator()
    if pnr.isdigit():
       pass
    else:
       return (translator.translate("Invalid Pnr",src="en",dest=language_input).text)
    selected_data={}
    if(len(pnr)==10):
      try:
        dbobj_user=dbsetup.connecttrainusers()
        selected_data = dbobj_user.find({ "pnr": {"$exists": True, "$eq": pnr}})
        
        
        for i in selected_data:
            selected_data=i
        if(selected_data!={} and  selected_data !=None and type(selected_data)==type({})):
            pdfmaking.generate_ticket(selected_data, "data/ticketpdf/indian_railway_ticket.pdf")
            return(translator.translate("Ticket downloaded",src="en",dest=language_input).text)
        else:
            return (translator.translate("Pnr not exist",src="en",dest=language_input).text)
        
      except Exception as e:

        print("Error:", e)
    else:
      return (translator.translate("Invalid Pnr",src="en",dest=language_input).text)
       
      
    


print(download_ticket(str(9892246557),"en"))