import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔐 Chave secreta para gerar tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")  # você pode trocar por algo mais seguro
ALGORITHM = "HS256"

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "instance", "fluxo.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
