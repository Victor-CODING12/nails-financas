from fastapi import Request, HTTPException, Depends
from ..models.usuario import Usuario
from ..models.base import SessionLocal
from ..utils.auth import decodificar_jwt


def usuario_atual_web(request: Request):
    """
    Obtém o usuário logado pelos dados armazenados no middleware.
    """

    if not request.state.user_email:
        raise HTTPException(status_code=401, detail="Não autenticado.")

    db = SessionLocal()

    usuario = db.query(Usuario).filter_by(email=request.state.user_email).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário inválido.")

    return usuario
