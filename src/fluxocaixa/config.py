import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # ==========================================
    # BANCO DE DADOS — CORREÇÃO PARA O RENDER
    # ==========================================

    SQLITE_PATH = os.path.join(BASE_DIR, "..", "..", "database.db")
    SQLITE_PATH = os.path.abspath(SQLITE_PATH)

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{SQLITE_PATH}"
    )
