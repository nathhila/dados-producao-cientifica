import os
import time
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.services.resumes_scopus import get_metadata, seconds_to_minutes
from src.services.joining_tables import creating_complete_table
from src.models.models import Base

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":

    print("INICIANDO PROCESSO")
    init_time = time.time()

    load_dotenv()
    SCOPUS_API_KEY = os.getenv("SCOPUS_API_KEY")

    if not SCOPUS_API_KEY:
        raise RuntimeError("SCOPUS_API_KEY não encontrada")

    producoes_path = "data/producoes.csv"
    topics_path = "data/producoes_topics.csv"

    if os.path.exists(producoes_path) and os.path.exists(topics_path):
        print("CSVs já existem. Lendo arquivos.")
        producoes_df = pd.read_csv(producoes_path, sep=";")
        topics_df = pd.read_csv(topics_path, sep=";")
    else:
        print("Extraindo dados da Scopus/OpenAlex...")
        producoes_df, topics_df = get_metadata(SCOPUS_API_KEY)

        producoes_df.to_csv(
            producoes_path,
            index=False,
            sep=";",
            encoding="utf-8-sig"
        )

        topics_df = topics_df.merge(
            producoes_df[["doi", "id_scopus"]],
            on="doi",
            how="left"
        )

        topics_df.to_csv(
            topics_path,
            index=False,
            sep=";",
            encoding="utf-8-sig"
        )

        print("CSVs gerados com sucesso")

    tempo = time.time() - init_time
    print(f"Tempo total: {seconds_to_minutes(tempo)} minutos")
    print("PROCESSO FINALIZADO")