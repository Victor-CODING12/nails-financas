from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from .auth import SECRET_KEY, ALGORITHM

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware para extrair empresa_id do token JWT e anexar à requisição"""

    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token") or request.headers.get("Authorization")

        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.state.user_email = payload.get("sub")
                request.state.empresa_id = payload.get("empresa_id")
            except JWTError:
                raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        # Se não houver token, segue sem erro (ex: página de login)
        response = await call_next(request)
        return response