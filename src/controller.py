def controller(lang):
    if(lang==None or lang==""):
        return ""
    elif(lang.lower()=="hindi"):
        return "hi"
    elif(lang.lower()=="english"):
        return "en"
    elif(lang.lower()=="marathi"):
        return "mr"
    elif(lang.lower()=="bangali" or lang.lower()=="bengali" or lang.lower()=="bangla"):
        return "bn"
    elif(lang.lower()=="russian"):
        return "ru"
    elif(lang.lower()=="spanish"):
        return "es"
    elif(lang.lower()=="telugu" or lang.lower()=="talugu" or lang.lower()=="telgu" or lang.lower()=="talgu"):
        return "te"
    elif(lang.lower()=="tamil" or lang.lower()=="temil" or lang.lower()=="tamill" or lang.lower()=="temil"):
        return "ta"
    else:
        return ""
 
