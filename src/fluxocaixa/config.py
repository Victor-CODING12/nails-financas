import os

class Config:
    # Se existir variável de ambiente DATABASE_URL (Render), usa ela.
    # Caso contrário, usa SQLite local para desenvolvimento.
    
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    if not SQLALCHEMY_DATABASE_URI:
        # Ambiente local (se quiser testar no PC)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        SQLITE_PATH = os.path.join(BASE_DIR, "..", "..", "database.db")
        SQLITE_PATH = os.path.abspath(SQLITE_PATH)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"
