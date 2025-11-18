# src/fluxocaixa/web/auth_routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session

from ..models import Usuario, Empresa, get_db
from ..utils.auth import hash_senha, criar_token
from . import templates  #  <<--- IMPORT CORRETO

router = APIRouter(prefix="/auth", tags=["Autenticação"])


# ============================================================
# 🔹 Tela de Login
# ============================================================
@router.get("/login")
def pagina_login(request: Request):
    # Se você quiser usar uma HTML real dentro de templates:
    return templates.TemplateResponse("login.html", {"request": request})

    # Caso estivesse usando /static/login.html (não recomendado):
    # return RedirectResponse("/static/login.html")


# ============================================================
# 🔹 Login (POST)
# ============================================================
@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    senha = form.get("senha")

    usuario = db.query(Usuario).filter_by(email=email).first()

    if not usuario or not hash_senha.verificar(senha, usuario.senha):
        return JSONResponse({"detail": "Credenciais inválidas."}, status_code=401)

    token = criar_token({"sub": usuario.email, "empresa_id": usuario.empresa_id})

    return {"access_token": token}


# ============================================================
# 🔹 Página de Registro (GET)
# ============================================================
@router.get("/register")
def pagina_register(request: Request):

    return templates.TemplateResponse("register.html", {"request": request})


# ============================================================
# 🔹 Registro (POST)
# ============================================================
@router.post("/register")
async def registrar(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    nome = form.get("nome")
    email = form.get("email")
    senha = form.get("senha")
    confirmar = form.get("confirmar_senha")
    empresa_nome = form.get("empresa")
    telefone = form.get("telefone")
    dias = form.getlist("dias[]")   #  <<--- corrigido (match com register.html)
    hora_abre = form.get("hora_abre")
    hora_fecha = form.get("hora_fecha")

    # -----------------------------
    # 🔎 Validações
    # -----------------------------
    if senha != confirmar:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "erro": "As senhas não coincidem."},
        )

    if db.query(Usuario).filter_by(email=email).first():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "erro": "E-mail já está em uso."},
        )

    # -----------------------------
    # 🏢 Criar empresa
    # -----------------------------
    empresa = Empresa(
        nome=empresa_nome,
        email=email,
        telefone=telefone,
        dias_funcionamento=",".join(dias),
        hora_abre=hora_abre,
        hora_fecha=hora_fecha,
    )

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    # -----------------------------
    # 👤 Criar usuário
    # -----------------------------
    usuario = Usuario(
        nome=nome,
        email=email,
        senha=hash_senha.gerar(senha),
        empresa_id=empresa.id,
        is_admin=True,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # -----------------------------
    # 🔐 Criar token e redirecionar
    # -----------------------------
    token = criar_token({"sub": usuario.email, "empresa_id": empresa.id})

    resp = RedirectResponse("/agendamento", status_code=302)
    resp.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)

    return resp
