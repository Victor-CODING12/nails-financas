import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..models import Usuario
from .token_utils import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def usuario_atual(token: str = Depends(oauth2_scheme)):
    payload = decodificar_token(token)

    if not payload or "user_id" not in payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    user = Usuario.query.get(payload["user_id"])

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return user
