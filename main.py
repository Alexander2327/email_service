from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings

from utils import make_amqp_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_amqp_consumer()
    yield
    # shutdown


main_app = FastAPI(
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
