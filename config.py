from dotenv import load_dotenv
import os

# CARREGAR VARIÁVEIS DO .env

load_dotenv()

# CONFIGURAÇÕES GERAIS

APP_NAME=os.getenv("APP_NAME")

APP_VERSION=os.getenv("APP_VERSION")

# BANCO DE DADOS

DATABASE_URL=os.getenv("DATABASE_URL")


