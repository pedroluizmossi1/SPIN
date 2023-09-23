from pydantic import BaseModel, Field, validator
from mongo_core import CONNECTIONS_COLLECTION
from bson import ObjectId

class Connections(BaseModel):
    name: str = Field(max_length=50, example="Oracle connection", default="")
    conn_type: str = Field(max_length=50, example="ORACLE", default="")
    host: str = Field(max_length=50, example="localhost", default="")
    port: str = Field(max_length=10, example="1521", default="")
    database: str = Field(max_length=50, example="xe", default="")
    username: str = Field(max_length=50, example="system", default="")
    password: str = Field(max_length=50, example="oracle", default="")
    
    class Body:
        openapi_examples={
                                    "ORACLE": {
                                        "summary": "Oracle connection",
                                        "value": {
                                            "name": "ORACLE",
                                            "conn_type": "ORACLE",
                                            "host": "localhost",
                                            "port": "1521",
                                            "database": "xe",
                                            "username": "system",
                                            "password": "oracle",
                                        },
                                    },
                                    "POSTGRESQL": {
                                        "summary": "PostgreSQL connection",
                                        "value": {
                                            "name": "POSTGRESQL",
                                            "conn_type": "POSTGRESQL",
                                            "host": "localhost",
                                            "port": "5432",
                                            "database": "postgres",
                                            "username": "postgres",
                                            "password": "postgres",
                                        },
                                    },
                                    "MYSQL": {
                                        "summary": "MySQL connection",
                                        "value": {
                                            "name": "MYSQL",
                                            "conn_type": "MYSQL",
                                            "host": "localhost",
                                            "port": "3306",
                                            "database": "mysql",
                                            "username": "root",
                                            "password": "root",
                                        },
                                    },
                                    "FIREBIRD": {
                                        "summary": "Firebird connection",
                                        "value": {
                                            "name": "FIREBIRD",
                                            "conn_type": "FIREBIRD",
                                            "host": "localhost",
                                            "port": "3050",
                                            "database": "C:/firebird/EMPLOYEE.FDB",
                                            "username": "SYSDBA",
                                            "password": "masterkey",
                                        },
                                    },
                                    "SQLITE": {
                                        "summary": "SQLite connection",
                                        "value": {
                                            "name": "SQLITE",
                                            "conn_type": "SQLITE",
                                            "host": "localhost",
                                            "port": "5432",
                                            "database": "postgres",
                                            "username": "postgres",
                                            "password": "postgres",
                                        },
                                    },
                                    "SQLSERVER": {
                                        "summary": "SQL Server connection",
                                        "value": {
                                            "name": "SQLSERVER",
                                            "conn_type": "SQLSERVER",
                                            "host": "localhost",
                                            "port": "1433",
                                            "database": "master",
                                            "username": "sa",
                                            "password": "admin123",
                                        },
                                    },
                                }
    
    def save(self):
        insert = CONNECTIONS_COLLECTION.insert_one(self.dict())
        return str(insert.inserted_id)
    
    def list(self):
        list_return = CONNECTIONS_COLLECTION.find()
        connection_list = []
        for connection in list_return:
            connection["_id"] = str(connection["_id"])
            connection_list.append(connection)
        return connection_list
    
    def get(self, id):
        connection = CONNECTIONS_COLLECTION.find_one({"_id": ObjectId(id)})
        if connection:
            return Connections(**connection)
        else:
            return False
        
    
    def create_index(self):
        try:
            CONNECTIONS_COLLECTION.create_index("name", unique=True)
            return True
        except:
            pass
            return False