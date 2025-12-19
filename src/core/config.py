from dotenv import load_dotenv

import os

# ==============================
# CONFIGURAÇÃO
# ==============================

load_dotenv()

AF_ID = os.getenv("AF_ID", "60030074") # ID DA UFMG

SCOPUS_PAGE_SIZE = int(os.getenv("SCOPUS_PAGE_SIZE", 25))
MAX_PER_QUERY = int(os.getenv("MAX_PER_QUERY", 5000))

START_YEAR = int(os.getenv("START_YEAR"))
END_YEAR = int(os.getenv("END_YEAR"))

SLEEP_SCOPUS = float(os.getenv("SLEEP_SCOPUS"))
SLEEP_OPENALEX = float(os.getenv("SLEEP_OPENALEX"))
