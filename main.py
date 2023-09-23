from api_core import app
from config_core import get_config
from mongo.endpoints_core import Endpoints
from mongo_core import Maindb

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=get_config('FASTAPI', 'host'), port=get_config('FASTAPI', 'port'))