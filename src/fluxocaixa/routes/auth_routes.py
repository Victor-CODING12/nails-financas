# src/fluxocaixa/routes/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..models import Usuario, Empresa, get_db
from ..auth.auth import verificar_senha, criar_token, hash_senha

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # No campo username do form, vamos usar o email
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos.",
        )

    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register(
    nome_empresa: str,
    email_empresa: str,
    nome_usuario: str,
    email_usuario: str,
    senha: str,
    db: Session = Depends(get_db),
):
    # Verifica se já existe empresa ou usuário com esse email
    if db.query(Empresa).filter(Empresa.email == email_empresa).first():
        raise HTTPException(status_code=400, detail="Já existe uma empresa com esse e-mail.")

    if db.query(Usuario).filter(Usuario.email == email_usuario).first():
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse e-mail.")

    # Cria empresa
    empresa = Empresa(
        nome=nome_empresa,
        email=email_empresa,
        cnpj=None,  # Preencher depois se quiser
    )
    db.add(empresa)
    db.flush()  # Garante que empresa.id exista

    # Cria usuário admin vinculado à empresa
    usuario = Usuario(
        nome=nome_usuario,
        email=email_usuario,
        senha=hash_senha(senha),
        is_admin=True,
        empresa_id=empresa.id,
    )
    db.add(usuario)
    db.commit()

    return {"message": "Empresa e usuário criados com sucesso!"}
