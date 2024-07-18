from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import CustomHTTPException

from app.api.users.router import router as users_router
from app.api.admins.router import router as admins_router
from app.api.accounts.router import router as account_router
from app.api.transactions.router import router as transactions_router
from app.api.auth.router import router as auth_router

app = FastAPI(
    title='Exercise',
    description='Проект для обучения',
    version='0.5'
)

@app.exception_handler(CustomHTTPException)
async def exception(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail}
    )

app.include_router(users_router)
app.include_router(admins_router)
app.include_router(account_router)
app.include_router(transactions_router)
app.include_router(auth_router)
