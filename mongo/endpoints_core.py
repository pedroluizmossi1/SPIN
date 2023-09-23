from pydantic import BaseModel, Field, validator
from mongo_core import ENDPOINTS_COLLECTION
from bson import ObjectId

class Endpoints(BaseModel):
    endpoint: str = Field (example="/endpoint", default="")
    method: str = Field (example="GET", default="")
    description: str = Field (example="Endpoint description", default="")
    status: str = Field (example="200", default="")
    response: str = Field (example="Response description", default="")
    active: bool = Field (example=True, default=True)
    cache: object = Field(example={
        "enabled": False,
        "ttl": 60,
        "type": "memory",
        "maxsize": 1000
    }, default={
        "enabled": False,
        "ttl": 60,
        "type": "memory",
        "maxsize": 1000
    })
    connection_id: str = Field(example="", default="")
    sql: str = Field(example="select * from dual", default="")

    @validator("connection_id")
    def validate_connection_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid connection id")
        return v
    
    class Body:
        openapi_examples = {
            "endpoint": {
                "summary": "Endpoint",
                "value": {
                    "endpoint": "/endpoint",
                    "method": "GET",
                    "description": "Endpoint description",
                    "status": "200",
                    "response": "Response description",
                    "active": True,
                    "cache": {
                        "enabled": False,
                        "ttl": 60,
                        "type": "memory",
                        "maxsize": 1000
                    },
                    "connection_id": "5f9b1f1e4e9a7f7a8e8e1b2c",
                    "sql": "select * from dual"
                },
            },
        }

    def save(self):  
        endpoint = ENDPOINTS_COLLECTION.insert_one(self.dict())
        return str(endpoint.inserted_id)
        
    def list(self):
        list_return = ENDPOINTS_COLLECTION.find()
        user_list = []
        for user in list_return:
            user["_id"] = str(user["_id"])
            user_list.append(user)
        return user_list
    
    def get(self, id):
        endpoint = ENDPOINTS_COLLECTION.find_one({"_id": ObjectId(id)})
        if endpoint:
            return Endpoints(**endpoint)
        else:
            return False
        
    def create_index(self):
        try:
            ENDPOINTS_COLLECTION.create_index("endpoint", unique=True)	
            return True
        except:
            pass
            return False