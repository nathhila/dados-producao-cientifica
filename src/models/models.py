from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, TEXT

Base = declarative_base()

class Producao(Base):
	__tablename__ = "producoes"

	id = Column(Integer, primary_key=True, autoincrement=True)
	autor = Column(String(255))
	titulo = Column(TEXT)
	id_scopus = Column(String(50))
	doi = Column(String(255))
	openalex_titulo = Column(TEXT)
	openalex_resumo = Column(TEXT)
	ano_publicacao = Column(String)

class Topicos(Base):
	__tablename__ = "producoes_topicos"

	id = Column(Integer, primary_key=True, autoincrement=True)
	doi = Column(String(255))
	topico = Column(String(255))
	id_scopus = Column(String(50))

class ProducaoCompleta(Base):
	__tablename__ = "producoes_tratadas"

	id = Column(Integer, primary_key=True, autoincrement=True)
	autor = Column(String(255))
	titulo = Column(TEXT)
	resumo = Column(TEXT)
	topico = Column(String(255))
	id_scopus = Column(String(50))