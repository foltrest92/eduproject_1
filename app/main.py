from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings

from app.api.users.router import router as users_router
from app.exceptions import CustomHTTPException

app = FastAPI()

@app.exception_handler(CustomHTTPException)
async def exception(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail}
    )


app.include_router(users_router)