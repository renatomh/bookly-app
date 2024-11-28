"""Custom middlewares for the application."""

import time
import logging

from fastapi import FastAPI
from fastapi.requests import Request

# Disabling default logger
logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middlware(app: FastAPI):

    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time

        # Creating the custom logger message
        message = f"{request.client.host}:{request.client.port} {request.method} {request.url.path} "
        message += f"{response.status_code} - completed after {processing_time}s"
        print(message)

        return response
