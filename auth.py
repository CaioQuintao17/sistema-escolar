from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "sistema_escolar_2026"

ALGORITHM = "HS256"

def criar_token(dados: dict):

    dados_token = dados.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    dados_token.update({
        "exp": expire
    })

    token = jwt.encode(
        dados_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token



def verificar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None