# 📊 Recuperação e Integração de Produções Científicas (Scopus + OpenAlex)

## Intenção do Projeto

Este projeto tem como objetivo **recuperar, integrar e tratar dados de produções científicas** de **qualquer universidade cadastrada na Scopus**, cruzando essas informações com a **OpenAlex** a partir do **DOI**.

O resultado é um conjunto de dados estruturado que permite:

* analisar a produção científica institucional;
* explorar resumos, tópicos e metadados enriquecidos;
* realizar análises posteriores em banco de dados relacional.

---

## Visão Geral do Pipeline

1. **Scopus**

   * Recupera todas as produções da universidade (via `AF_ID`)
   * Considera um intervalo de anos configurável

2. **OpenAlex**

   * Usa o **DOI** como chave de integração
   * Recupera título, resumo, número de citações e tópicos

3. **Persistência**

   * Geração de dois CSVs:

     * Produções
     * Tópicos (normalizados)
   * Inserção em banco PostgreSQL
   * Join das tabelas para criar uma **tabela final tratada**

---

## Saídas do Projeto

### CSVs gerados

* `producoes.csv`

  * autor
  * título (Scopus)
  * DOI
  * título (OpenAlex)
  * resumo

* `producoes_topics.csv`

  * DOI
  * id_scopus
  * tópico

### Banco de Dados

* Tabelas intermediárias (Scopus / OpenAlex)
* Tabela final tratada com dados integrados

---

## Variáveis de Ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto a partir do env.example.txt

---

## Como Rodar o Projeto

### Pré-requisitos

* Python 3.12+
* PostgreSQL 17

### Passos

1. Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências dentro da venv:

```bash
pip install -r requirements.txt
```

3. Execute o pipeline manualmente:

```bash
python -m main          # gera os CSVs
python -m init_db       # cria as tabelas
psql -h localhost -p <porta> -U <usuario> -d <database> -f src/models/insert_csv.sql # insere os csvs na tabela
python -m db_complet    # cria a tabela final tratada
```
---

Se quiser adaptar o projeto para outra instituição, basta alterar o `AF_ID` no `.env`.
