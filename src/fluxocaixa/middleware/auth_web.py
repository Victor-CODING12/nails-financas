from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..utils.auth import decodificar_jwt    # ✔️ Import correto
from ..models import Usuario
from ..models.base import SessionLocal


class AuthWebMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        rota = request.url.path

        # Rotas públicas
        rotas_livres = [
            "/auth/login",
            "/auth/register",
            "/static/",
        ]

        # Se for rota livre → libera
        if any(rota.startswith(r) for r in rotas_livres):
            return await call_next(request)

        # Recupera token do cookie
        token = request.cookies.get("access_token")

        if not token:
            return RedirectResponse("/auth/login")

        # Remove prefixo "Bearer "
        token = token.replace("Bearer ", "")

        # Decodifica JWT
        payload = decodificar_jwt(token)

        if not payload:
            return RedirectResponse("/auth/login")

        email = payload.get("sub")
        empresa_id = payload.get("empresa_id")

        if not email or not empresa_id:
            return RedirectResponse("/auth/login")

        # Busca usuário no banco
        session = SessionLocal()
        usuario = session.query(Usuario).filter_by(email=email).first()
        session.close()

        if not usuario:
            return RedirectResponse("/auth/login")

        # Armazena usuário na request
        request.state.usuario = usuario

        return await call_next(request)
