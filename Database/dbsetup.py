




from pymongo.mongo_client import MongoClient
#For train details
database_namet="Train"
collection_namet="Train_details"
#for user details
database_nameu="Train_users"
collection_nameu="User_details"


def connecttrain():
    uri = "mongodb+srv://vinit_dubey:1860Amul@cluster0.zjwfiov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    n=client[database_namet][collection_namet]
    return n
def connecttrainusers():
    uri = "mongodb+srv://vinit_dubey:1860Amul@cluster0.zjwfiov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)
    n=client[database_nameu][collection_nameu]
    return n

connecttrainusers()