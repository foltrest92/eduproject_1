from fastapi import Request, Response

from app.api.auth.dao import AuthDAO
from app.config import settings
from app.exceptions import NoLoginException, NoPermissionException


async def is_admin_permission(request: Request, response: Response) -> bool:
    refresh_token = request._cookies.get('refresh_token', False)
    access_token = request._cookies.get('access_token', False)
    if not refresh_token and not access_token:
        raise NoLoginException
    try:
        access_payload = await AuthDAO.check_access_token(access_token)
    except:
        try:
            access_token = await AuthDAO.get_access_token(refresh_token)
        except:
            response.set_cookie(key='access_token', max_age=0)
            response.set_cookie(key='refresh_token', max_age=0)
            raise NoLoginException
        else:
            response.set_cookie(key='access_token', value=access_token, max_age=settings.ACCESS_TOKEN_AGE)
            access_payload = await AuthDAO.check_access_token(access_token)

    if access_payload['role'] == 'admin':
        return True
    else:
        raise NoPermissionException

        
        
