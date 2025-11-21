from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import db_conn
from helpers.logging import logger
from .initializer import init
from apps.change_name_app.router import router as router_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

logger.info("Starting application initialization...")
init(app, db_conn.engine)
logger.info("Initialization...")

app.include_router(router_data)
