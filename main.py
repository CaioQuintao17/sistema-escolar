from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from config import APP_NAME, APP_VERSION

from database import (
    engine,
    get_db,
    SessionLocal
)

from models import (
    Base,
    Aluno,
    Usuario
)

from schemas import (
    AlunoCreate,
    UsuarioCreate,
    LoginRequest
)

from auth import (
    criar_token,
    verificar_token
)

# ==================================================
# CONFIGURAÇÕES
# ==================================================

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

security = HTTPBearer()

# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

# ==================================================
# AUTENTICAÇÃO
# ==================================================

def usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):

    token = credenciais.credentials

    dados = verificar_token(token)

    if not dados:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return dados

# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():

    return {
        "mensagem": APP_NAME
    }

# ==================================================
# USUÁRIOS
# ==================================================

@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate):

    db = SessionLocal()

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=usuario.senha
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    return novo_usuario

# ==================================================
# LOGIN
# ==================================================

@app.post("/login")
def login(usuario: LoginRequest):

    db = SessionLocal()

    usuario_db = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if not usuario_db:

        return {
            "erro": "Usuário não encontrado"
        }

    if usuario_db.senha != usuario.senha:

        return {
            "erro": "Senha incorreta"
        }

    token = criar_token(
        {
            "email": usuario_db.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ==================================================
# ALUNOS
# ==================================================

@app.post("/alunos")
def criar_aluno(
    aluno: AlunoCreate,
    db: Session = Depends(get_db)
):

    novo_aluno = Aluno(
        nome=aluno.nome,
        turma=aluno.turma,
        nota=aluno.nota
    )

    db.add(novo_aluno)

    db.commit()

    db.refresh(novo_aluno)

    return novo_aluno


@app.get("/alunos")
def listar_alunos(
    usuario=Depends(usuario_logado),
    db: Session = Depends(get_db)
):

    return db.query(Aluno).all()


@app.get("/alunos/{aluno_id}")
def buscar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):

    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if not aluno:

        return {
            "erro": "Aluno não encontrado"
        }

    return aluno


@app.put("/alunos/{aluno_id}")
def atualizar_aluno(
    aluno_id: int,
    aluno_atualizado: AlunoCreate,
    db: Session = Depends(get_db)
):

    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if not aluno:

        return {
            "erro": "Aluno não encontrado"
        }

    aluno.nome = aluno_atualizado.nome
    aluno.turma = aluno_atualizado.turma
    aluno.nota = aluno_atualizado.nota

    db.commit()

    db.refresh(aluno)

    return aluno


@app.delete("/alunos/{aluno_id}")
def deletar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):

    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if not aluno:

        return {
            "erro": "Aluno não encontrado"
        }

    db.delete(aluno)

    db.commit()

    return {
        "mensagem": "Aluno deletado com sucesso"
    }