import pymongo
from config_core import get_config, update_config
from bson import ObjectId

conn = pymongo.MongoClient("mongodb+srv://spin:spin@cluster1.pvl7w4l.mongodb.net/?retryWrites=true&w=majority")

DB = conn["main"]
ENDPOINTS_COLLECTION = DB["endpoints"]
CONNECTIONS_COLLECTION = DB["connections"]

if get_config("MONGODB","create_index") == "True":
    update_config("MONGODB","create_index","False")
    ENDPOINTS_COLLECTION.create_index("endpoint", unique=True)
    CONNECTIONS_COLLECTION.create_index("name", unique=True)
    
    

class Maindb:
    db = None
    def __init__(self):
        self.db = DB

    def get_db(self):
        return self.db

    def get_endpoints_collection(self):
        return ENDPOINTS_COLLECTION
    