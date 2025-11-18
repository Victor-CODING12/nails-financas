from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    scoped_session,
    Query,
)
from fastapi import HTTPException

from ..config import Config


# ==========================================================
# CONFIGURAÇÃO DO ENGINE — CORRIGIDO
# SQLite exige check_same_thread=False para funcionar no FastAPI
# ==========================================================
connect_args = {}

if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
)


# ==========================================================
# SESSIONLOCAL + BASE
# ==========================================================
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)

Base = declarative_base()
Base.query = SessionLocal.query_property()


# ==========================================================
# GET_OR_404 HELPER
# ==========================================================
def _query_get_or_404(self: Query, ident, description=None):
    obj = self.get(ident)
    if obj is None:
        if description is None:
            model = self.column_descriptions[0]["type"].__name__
            description = f"{model} not found"
        raise HTTPException(status_code=404, detail=description)
    return obj


Query.get_or_404 = _query_get_or_404


# ==========================================================
# OBJETO DB COMPATÍVEL DO FLASK-SQLALCHEMY
# ==========================================================
class _DB:
    def __init__(self):
        self.session = SessionLocal

    def create_all(self):
        Base.metadata.create_all(bind=engine)

    def drop_all(self):
        Base.metadata.drop_all(bind=engine)


db = _DB()


# ==========================================================
# DEPENDÊNCIA PARA ROTAS
# ==========================================================
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
