"""
load.py
-------
Responsabilidade única: persistir o DataFrame transformado no PostgreSQL.

Recebe: pd.DataFrame vindo do transform.py
Retorna: None (efeito colateral: dados no banco)

Estratégia de carga: replace
  A cada execução, a tabela é limpa e recarregada com dados frescos.
  Motivo: a Fake Store API é estática — append acumularia duplicatas.

Por que to_sql e não INSERT via ORM?
  to_sql é otimizado para carga em bulk com Pandas — muito mais rápido
  do que fazer session.add() produto por produto via ORM.
  ORM fica reservado para queries (queries.py).
"""

import logging
from datetime import datetime, timezone

import pandas as pd

from app.database.connection import engine

logger = logging.getLogger(__name__)


def load_products(df: pd.DataFrame) -> None:
    """
    Persiste o DataFrame de produtos no PostgreSQL.

    Parâmetros:
        df: pd.DataFrame retornado por transform.transform_products()

    Lança:
        RuntimeError — se o DataFrame estiver vazio
        Exception   — propaga erros de conexão ou escrita no banco
    """
    if df.empty:
        raise RuntimeError("DataFrame vazio — nada para carregar no banco.")

    # Adiciona timestamps de controle antes de carregar
    now = datetime.now(timezone.utc)
    df = df.copy()
    df["created_at"] = now
    df["updated_at"] = now

    logger.info(f"Carregando {len(df)} produtos no banco...")

    df.to_sql(
        name="products",
        con=engine,
        if_exists="replace",  # limpa e recarrega a cada execução
        index=False,          # não salva o índice do DataFrame como coluna
        method="multi",       # insert em batch — mais eficiente que linha a linha
    )

    logger.info("Carga concluída com sucesso.")
    print(f"✅ {len(df)} produtos carregados no banco.")