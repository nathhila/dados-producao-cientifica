import requests
import os
import pandas as pd
import time

from tqdm import tqdm
from src.core.config import AF_ID, SCOPUS_PAGE_SIZE, MAX_PER_QUERY, START_YEAR, END_YEAR, SLEEP_SCOPUS, SLEEP_OPENALEX

# ==============================
# UTILIDADES
# ==============================
def seconds_to_minutes(seconds):
    return round(seconds / 60, 2)

def normalize_id_scopus(base_df):

    base_df["id_scopus"] = base_df["id_scopus"].str.replace(
        "SCOPUS_ID:", "", regex=False
    )
    return base_df

# ==============================
# OPENALEX
# ==============================
def fetch_openalex_metadata(dois):
    """
    Retorna dados normalizados da OpenAlex:
    - tabela 1: metadados da produção
    - tabela 2: tópicos (1 linha por tópico)
    """

    works_rows = []
    topics_rows = []

    session = requests.Session()
    session.headers.update({
        "User-Agent": "bibliometria-ufmg/1.0 (email@ufmg.br)"
    })

    for doi in tqdm(dois, desc="OpenAlex (metadata)", unit="doi"):
        try:
            url = f"https://api.openalex.org/works/https://doi.org/{doi}"
            r = session.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()

            # ===== ABSTRACT =====
            inv = data.get("abstract_inverted_index")
            if inv:
                words = {}
                for word, positions in inv.items():
                    for p in positions:
                        words[p] = word
                abstract = " ".join(words[i] for i in sorted(words))
            else:
                abstract = None

            # ===== METADADOS DA PRODUÇÃO =====
            works_rows.append({
                "doi": doi,
                "openalex_titulo": data.get("title"),
                "resumo": abstract,
                "ano_publicacao": data.get("publication_year")
            })

            # ===== TÓPICOS (1 LINHA POR TÓPICO) =====
            for t in data.get("topics", []):
                topics_rows.append({
                    "doi": doi,
                    "topico": t.get("display_name")
                })

        except Exception:
            continue

    return (
        pd.DataFrame(works_rows),
        pd.DataFrame(topics_rows)
    )


# ==============================
# SCOPUS (POR ANO)
# ==============================

def fetch_scopus_year(api_key, year):
    """
    Busca TODOS os registros Scopus da UFMG para um ano específico
    """

    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json"
    }

    session = requests.Session()
    all_entries = []
    start = 0

    while start < MAX_PER_QUERY:

        params = {
            "query": f"AF-ID({AF_ID}) AND PUBYEAR = {year}",
            "view": "STANDARD",
            "start": start,
            "count": SCOPUS_PAGE_SIZE
        }

        r = session.get(url, params=params, headers=headers)
        r.raise_for_status()

        data = r.json()
        entries = data["search-results"].get("entry", [])

        if not entries:
            break

        all_entries.extend(entries)
        start += SCOPUS_PAGE_SIZE

        time.sleep(SLEEP_SCOPUS)

    if not all_entries:
        return pd.DataFrame()

    df = pd.DataFrame(all_entries)

    df = df.rename(columns={
        "dc:creator": "autor",
        "dc:title": "titulo",
        "dc:identifier": "id_scopus",
        "prism:doi": "doi"
    })
    print(f"Registros Scopus UFMG em {year}: {len(df)}")

    return df[["autor", "titulo", "id_scopus", "doi"]] # todas as producoes da ufmg em um determinado ano

# ==============================
# PIPELINE PRINCIPAL
# ==============================

def get_metadata(SCOPUS_API_KEY):

    print("Extraindo metadados da Scopus (UFMG)")

    all_dfs = []
    years = range(START_YEAR, END_YEAR + 1)

    for year in tqdm(years, desc="Scopus (anos)", unit="ano"):
        df_year = fetch_scopus_year(SCOPUS_API_KEY, year)
        if not df_year.empty:
            all_dfs.append(df_year)

    base_df = pd.concat(all_dfs, ignore_index=True)

    # ==============================
    # NORMALIZAÇÃO
    # ==============================
    base_df = normalize_id_scopus(base_df)

    # ==============================
    # OPENALEX
    # ==============================
    dois = (
        base_df["doi"]
        .dropna()
        .unique()
        .tolist()
    )

    print(f"\nDOIs únicos para buscar OpenAlex: {len(dois)}")

    works_df, topics_df = fetch_openalex_metadata(dois)

    # ===== junta metadados OpenAlex à produção =====
    base_df = base_df.merge(
        works_df,
        on="doi",
        how="left"
    )

    return base_df, topics_df

