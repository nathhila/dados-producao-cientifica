from src.models.models import Producao, Topicos
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import pandas as pd

# load_dotenv()

def creating_complete_table(db, table_name, engine):

	resultado = db.query(Producao.autor,
					  	Producao.titulo,
						Producao.openalex_resumo,
						Topicos.topico,
						Producao.id_scopus).join(Topicos, Producao.id_scopus == Topicos.id_scopus).all()

	df = pd.DataFrame(resultado, columns=['autor', 'titulo', 'resumo', 'topico', 'id_scopus'])
	
	df.to_sql(table_name, engine, if_exists='append', index=False)

	return df
