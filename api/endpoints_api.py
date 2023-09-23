from fastapi import routing, HTTPException, Body
from typing import Annotated
from mongo.endpoints_core import Endpoints
from mongo.connections_core import Connections
from database_bridge import Engine



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
            engine = Engine(connection_id=endpoint.connection_id)
            df = engine.execute(endpoint.sql)
            return df.to_dict(orient="records")
        else:
            return HTTPException(status_code=500, detail="Endpoint not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))