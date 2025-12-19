from dotenv import load_dotenv
from init_db import engine
from sqlalchemy.orm import sessionmaker
from src.services.joining_tables import creating_complete_table
import os


if __name__ == "__main__":

    load_dotenv()

    # =================================================
    # INSERINDO NA NOVA TABELA AS PRODUÇÕES JÁ TRATADAS
    # =================================================

    Session = sessionmaker(bind=engine)
    db = Session()

    resultado = creating_complete_table(
        db,
        "producoes_tratadas",
        engine
    )

    print(resultado)
    print("\nPIPELINE FINALIZADO COM SUCESSO")
