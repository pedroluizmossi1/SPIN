from fastapi import routing, HTTPException, Body
from mongo.connections_core import Connections
from typing import Annotated


connections_router = routing.APIRouter(
    prefix="/connections",
    tags=["connections"],
    responses={404: {"description": "Not found"}},
)

@connections_router.post("/create")
async def create_endpoint(connection:  Annotated[
                            Connections,
                            Body(
                                openapi_examples= Connections.Body.openapi_examples,
                            )
                            
                        ]):
    try:
        endpoint = Connections(**connection.dict()).save()
        return {"success": True, "message": "Connection created successfully", "data": endpoint}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@connections_router.get("/list")
async def list_connections():
    try:
        connections = Connections().list()
        return connections
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@connections_router.get("/get/{id}")
async def get_connection(id: str):
    try:
        connection = Connections().get(id)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))