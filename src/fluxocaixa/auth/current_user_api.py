from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .token_utils import decodificar_token
from ..models import Usuario

bearer_scheme = HTTPBearer()


async def usuario_atual_api(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Obtém o usuário autenticado via token JWT para chamadas de API.
    """
    token = credentials.credentials
    payload = decodificar_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    user = Usuario.query.get(payload["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return user
