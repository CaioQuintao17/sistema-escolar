from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Aluno(Base):

    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    turma = Column(String, nullable=False)

    nota = Column(Float, nullable=False)
    
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    
    nome = Column(String, nullable=False)
    
    email = Column(
        String,
        unique=True,
        nullable=False
    )
    
    senha = Column(
        String,
        nullable=False
    )
    
    
    