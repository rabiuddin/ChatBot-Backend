from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.app.utils.response_builder_utils import ResponseBuilder

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request: Request, exc):
    response = ResponseBuilder().set_success(False).setStatusCode(status.HTTP_429_TOO_MANY_REQUESTS).set_error("Rate Limit has exceeded, please try again later.").build()
    return JSONResponse(content=response)