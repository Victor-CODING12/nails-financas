from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse
from fastapi import Request
from jose import jwt, JWTError
from ..config import SECRET_KEY, ALGORITHM


# Rotas que NÃO precisam de login
ROTAS_PUBLICAS = {
    "/auth/login",
    "/auth/register",
    "/static",
    "/favicon.ico"
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        # Se for rota pública → libera
        if any(path.startswith(r) for r in ROTAS_PUBLICAS):
            return await call_next(request)

        # Pega token do cookie
        token = request.cookies.get("access_token")

        if not token:
            return RedirectResponse("/auth/login")

        # Remove o "Bearer " se tiver
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_email = payload.get("sub")
            request.state.empresa_id = payload.get("empresa_id")

        except JWTError:
            return RedirectResponse("/auth/login")

        return await call_next(request)
