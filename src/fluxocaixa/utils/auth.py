import jwt
import datetime
from jwt import ExpiredSignatureError, InvalidTokenError

SECRET_KEY = "SUA_CHAVE_SECRETA_AQUI"
ALGORITHM = "HS256"

def criar_token(data: dict, expira_em_horas=24):
    """Cria um token JWT"""
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=expira_em_horas)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_jwt(token: str):
    """Decodifica o JWT e retorna o payload"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None

def hash_senha(senha: str):
    import hashlib
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, senha_hash: str):
    return hash_senha(senha) == senha_hash
