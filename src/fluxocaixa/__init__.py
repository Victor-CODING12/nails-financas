from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .models import db
from .utils.formatters import format_currency
from .web import router, templates

def create_app() -> FastAPI:
    app = FastAPI()

    # cria tabelas
    db.create_all()

    # configura filtros Jinja2
    templates.env.filters['format_currency'] = format_currency

    # rotas
    app.include_router(router)

    # rotas de login
    from .web import auth_routes
    app.include_router(auth_routes.router)

    # arquivos estáticos
    static_folder = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_folder), name="static")

    return app
