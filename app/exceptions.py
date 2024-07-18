from fastapi import status


class CustomHTTPException(Exception):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    detail="Unknown"
    def __init__(self) -> None:
        super().__init__(NoFoundException.status_code, NoFoundException.detail)


class TokenIsInvalidException(CustomHTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Invalid access_token"


class TokenIsExpiredException(CustomHTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Access_token is expired"

class UserIsAlreadyExist(CustomHTTPException):
    status_code=status.HTTP_409_CONFLICT
    detail='User is already exist'

class TransactionIsAlreadyCommitedException(CustomHTTPException):
    status_code=status.HTTP_409_CONFLICT
    detail='Transaction is already commited'

class InvalidPasswordOrLoginException(CustomHTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid login or password"

class NoLoginException(CustomHTTPException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="UNAUTHORIZED"

class NoPermissionException(CustomHTTPException):
    status_code=status.HTTP_403_FORBIDDEN
    detail="No permission"

class NoFoundException(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail="No found"

class UnknownException(CustomHTTPException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "WTF"

class InvalidSignatureException(CustomHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Invalid signature"