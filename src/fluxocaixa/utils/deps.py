from fastapi import Depends, HTTPException, Cookie
from jose import jwt, JWTError
from ..utils.auth import SECRET_KEY, ALGORITHM
from ..models.usuario import Usuario
from ..models.base import get_db
from sqlalchemy.orm import Session

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    """Obtém o usuário logado com base no cookie JWT"""
    if not access_token:
        raise HTTPException(status_code=401, detail="Token de autenticação ausente")

    token = access_token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        empresa_id = payload.get("empresa_id")

        if email is None or empresa_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user