from fastapi import FastAPI

from api.endpoints_api import endpoints_router
from api.connections_api import connections_router

app = FastAPI()

app.include_router(endpoints_router)
app.include_router(connections_router)


