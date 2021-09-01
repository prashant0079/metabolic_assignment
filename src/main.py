import os
from datetime import datetime
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.requests import Request

from src.const.api_const import API_TITLE, API_DESCRIPTION, API_VERSION
from src.router.v1 import api_v1

api = FastAPI(title=API_TITLE,
              description=API_DESCRIPTION,
              version=API_VERSION)

api.include_router(api_v1, prefix='/v1')

api.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@api.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()

    # modify request
    response = await call_next(request)

    # modify response
    execution_time = (datetime.now() - start_time).seconds
    response.headers["x-execution_time"] = str(execution_time)

    return response
