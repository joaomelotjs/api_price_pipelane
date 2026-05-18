"""
queries.py
----------
Consultas reutilizáveis para o dashboard Streamlit.

Por que SQL direto (text()) em vez de ORM?
  Consultas analíticas com GROUP BY, AVG, MIN, MAX ficam mais legíveis
  em SQL puro. ORM é mais adequado para CRUD simples.

Todas as funções retornam list[dict] — formato direto para o Streamlit
converter em DataFrame ou exibir em tabelas.
"""

import logging

import pandas as pd
from sqlalchemy import text

from app.database.connection import get_session

logger = logging.getLogger(__name__)


def get_all_products() -> pd.DataFrame:
    """
    Retorna todos os produtos ordenados por categoria e preço.
    """
    sql = text("""
        SELECT
            id,
            title,
            price,
            category,
            description,
            image,
            rating_rate,
            rating_count
        FROM products
        ORDER BY category, price
    """)

    with get_session() as session:
        result = session.execute(sql)
        rows = result.mappings().all()

    return pd.DataFrame(rows)


def get_avg_price_by_category() -> pd.DataFrame:
    """
    Retorna o preço médio por categoria, ordenado do maior para o menor.
    """
    sql = text("""
        SELECT
            category,
            ROUND(AVG(price)::numeric, 2) AS avg_price,
            COUNT(*) AS total_products
        FROM products
        GROUP BY category
        ORDER BY avg_price DESC
    """)

    with get_session() as session:
        result = session.execute(sql)
        rows = result.mappings().all()

    return pd.DataFrame(rows)


def get_price_range_by_category() -> pd.DataFrame:
    """
    Retorna o produto mais caro e mais barato por categoria.
    """
    sql = text("""
        SELECT
            category,
            MAX(price) AS max_price,
            MIN(price) AS min_price,
            ROUND((MAX(price) - MIN(price))::numeric, 2) AS price_range
        FROM products
        GROUP BY category
        ORDER BY category
    """)

    with get_session() as session:
        result = session.execute(sql)
        rows = result.mappings().all()

    return pd.DataFrame(rows)


def get_top_rated_products(limit: int = 5) -> pd.DataFrame:
    """
    Retorna os produtos com melhor avaliação.

    Parâmetros:
        limit: quantidade de produtos a retornar (padrão: 5)
    """
    sql = text("""
        SELECT
            id,
            title,
            category,
            price,
            rating_rate,
            rating_count
        FROM products
        ORDER BY rating_rate DESC, rating_count DESC
        LIMIT :limit
    """)

    with get_session() as session:
        result = session.execute(sql, {"limit": limit})
        rows = result.mappings().all()

    return pd.DataFrame(rows)