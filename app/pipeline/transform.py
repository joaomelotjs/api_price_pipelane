"""
transform.py
------------
Responsabilidade única: limpar e transformar dados brutos em DataFrame pronto
para persistência.

Recebe: list[dict] vinda do extract.py
Retorna: pd.DataFrame com colunas alinhadas ao modelo Product do banco

Transformações aplicadas:
  1. Converte lista de dicionários em DataFrame
  2. Extrai rating.rate e rating.count do dicionário aninhado
  3. Remove a coluna rating original (já extraída)
  4. Garante tipos corretos de cada coluna
  5. Remove linhas com campos obrigatórios nulos (title, price, category)
  6. Reseta o índice

Por que extrair rating em vez de ignorar?
  rate e count são métricas analíticas relevantes para o dashboard
  (ex: média de avaliação por categoria, produtos mais avaliados).
  Ignorá-los seria desperdiçar dados já disponíveis.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def transform_products(raw_data: list[dict]) -> pd.DataFrame:
    """
    Transforma lista de produtos brutos em DataFrame limpo.

    Parâmetros:
        raw_data: list[dict] retornada por extract.fetch_products()

    Retorna:
        pd.DataFrame com as colunas:
        id, title, price, category, description, image, rating_rate, rating_count
    """
    logger.info(f"Iniciando transformação de {len(raw_data)} produtos.")

    # 1. Lista de dicionários → DataFrame
    df = pd.DataFrame(raw_data)

    # 2. Extrair campos do dicionário aninhado rating
    # rating vem como: {'rate': 3.9, 'count': 120}
    df["rating_rate"]  = df["rating"].apply(lambda x: x.get("rate")  if isinstance(x, dict) else None)
    df["rating_count"] = df["rating"].apply(lambda x: x.get("count") if isinstance(x, dict) else None)

    # 3. Remover coluna original aninhada
    df = df.drop(columns=["rating"])

    # 4. Garantir tipos corretos
    df["id"]           = df["id"].astype(int)
    df["price"]        = df["price"].astype(float)
    df["rating_rate"]  = pd.to_numeric(df["rating_rate"],  errors="coerce")
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce").astype("Int64")

    # 5. Remover linhas com campos obrigatórios nulos
    before = len(df)
    df = df.dropna(subset=["title", "price", "category"])
    dropped = before - len(df)
    if dropped > 0:
        logger.warning(f"{dropped} linha(s) removida(s) por campos obrigatórios nulos.")

    # 6. Resetar índice
    df = df.reset_index(drop=True)

    logger.info(f"Transformação concluída. {len(df)} produtos prontos para carga.")
    return df