from pydantic import BaseModel

class AlunoCreate(BaseModel):

    nome: str
    turma: str
    nota: float
    
class UsuarioCreate(BaseModel):
    
    nome: str
    email: str
    senha: str

class LoginRequest(BaseModel):
    
    email: str
    senha: str
    
    
    
    