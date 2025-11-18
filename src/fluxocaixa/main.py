# src/fluxocaixa/main.py

from fastapi import FastAPI
from .models import db
from .web import templates

# IMPORTA O MIDDLEWARE CORRETO
from .middleware.auth_web import AuthWebMiddleware

# IMPORTA SUAS ROTAS
from .web.auth_routes import router as auth_router
from .routes.fluxo_caixa_routes import router as fluxo_router
# Se tiver mais rotas, adicione aqui

# ================================
# APP FASTAPI
# ================================
app = FastAPI(title="Nails Designer - Fluxo de Caixa")

# ================================
# MIDDLEWARE DE AUTENTICAÇÃO WEB
# ================================
app.add_middleware(AuthWebMiddleware)

# ================================
# ROTAS
# ================================
app.include_router(auth_router)
app.include_router(fluxo_router)

# Se quiser outras rotas:
# app.include_router(agendamentos_router)
# app.include_router(servicos_router)

# ================================
# CRIA BANCO AO INICIAR
# ================================
@app.on_event("startup")
def on_startup():
    db.create_all()
