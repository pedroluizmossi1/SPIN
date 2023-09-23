from fastapi import routing, HTTPException, Body
from typing import Annotated
from mongo.endpoints_core import Endpoints
from mongo.connections_core import Connections

from sqlalchemy import create_engine, text


endpoints_router = routing.APIRouter(
    prefix="/endpoints",
    tags=["endpoints"],
    responses={404: {"description": "Not found"}},
)

@endpoints_router.post("/create")
async def create_endpoint(endpoint: Annotated[
                                    Endpoints,
                                    Body(
                                        openapi_examples= Endpoints.Body.openapi_examples,
                                    )]
                                    ):
    if Connections().get(endpoint.connection_id):
        try:
            endpoint = endpoint.save()
            return {"success": True, "message": "Endpoint created successfully", "data": endpoint}
        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))
    else:
        return HTTPException(status_code=500, detail="Connection not found")
    
@endpoints_router.get("/list")
async def list_endpoints():
    try:
        endpoints = Endpoints().list()
        return endpoints
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@endpoints_router.get("/get/{id}")
async def get_endpoint(id: str):
    try:
        endpoint = Endpoints().get(id)
        return endpoint
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@endpoints_router.get("/execute/{id}")
async def execute_endpoint(id: str):
    try:
        endpoint = Endpoints().get(id)
        if endpoint:
            connection = Connections().get(endpoint.connection_id)
            if connection:
                if connection.conn_type == "POSTGRESQL":
                    engine = create_engine(f'postgresql://{connection.username}:{connection.password}@{connection.host}/{connection.database}')
                    with engine.connect() as conn:
                        sql = text(endpoint.sql)
                        sql = conn.execute(sql)
                        print(sql)
            else:
                return HTTPException(status_code=500, detail="Connection not found")
        else:
            return HTTPException(status_code=500, detail="Endpoint not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))