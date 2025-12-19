"""
SCRIPT RESPONSÁVEL POR CRIAR AS TABELAS ESTABELECIDAS EM MODELS NO BANCO DE DADOS
"""

from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

from src.models.models import Base

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URI"))

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso")
