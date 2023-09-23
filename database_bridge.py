from sqlalchemy import create_engine, text, MetaData
from mongo.connections_core import Connections
import pandas as pd

class Engine:
    def __init__(self, connection_id: str = None, host: str = None, port: str = None, username: str = None, password: str = None, database: str = None, conn_type: str = None):
        if connection_id:
            connection = Connections().get(connection_id)
            self.host = connection.host
            self.port = connection.port
            self.username = connection.username
            self.password = connection.password
            self.database = connection.database
            self.conn_type = connection.conn_type
        else:
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            self.database = database
            self.conn_type = conn_type
        self.engine = self.get_engine()
        
    def execute(self, sql: str):
        with self.engine.connect() as conn:
            sql = text(sql)
            result = conn.execute(sql)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            df = df.fillna('')
            return df
        
    def get_engine(self):
        if self.conn_type == "POSTGRESQL":
            engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}')
            return engine
        elif self.conn_type == "MYSQL":
            engine = create_engine(f'mysql://{self.username}:{self.password}@{self.host}')
            return engine
        elif self.conn_type == "MSSQL":
            engine = create_engine(f'mssql://{self.username}:{self.password}@{self.host}')
            return engine
        elif self.conn_type == "SQLITE":
            engine = create_engine(f'sqlite:///{self.host}')
            return engine
        elif self.conn_type == "ORACLE":
            engine = create_engine(f'oracle://{self.username}:{self.password}@{self.host}')
            return engine
        else:
            return None
        
