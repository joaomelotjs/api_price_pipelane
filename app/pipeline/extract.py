"""
extract.py
----------
Responsabilidade única: buscar dados brutos da Fake Store API.

Não transforma, não limpa, não persiste.
Retorna os dados exatamente como a API entrega — lista de dicionários.

Por que retornar lista de dicionários e não DataFrame?
  Manter a separação clara entre camadas:
  - extract  → dados brutos (list[dict])
  - transform → dados limpos (DataFrame)
  - load     → persistência (PostgreSQL)
"""

import logging

import requests

from app.config.settings import settings

logger = logging.getLogger(__name__)


def fetch_products() -> list[dict]:
    """
    Chama a Fake Store API e retorna lista de produtos brutos.

    Retorna:
        list[dict] — cada dict representa um produto com os campos:
        id, title, price, category, description, image, rating

    Lança:
        RuntimeError — se a API retornar status != 200
        requests.exceptions.ConnectionError — se não conseguir conectar
    """
    logger.info(f"Chamando API: {settings.API_URL}")

    headers = {"User-Agent": "api-price-pipeline/1.0"}

    try:
        response = requests.get(settings.API_URL, headers=headers, timeout=10)
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Não foi possível conectar à API: {e}")
    except requests.exceptions.Timeout:
        raise RuntimeError("A API não respondeu dentro do tempo limite (10s).")

    if response.status_code != 200:
        raise RuntimeError(
            f"API retornou status inesperado: {response.status_code}"
        )

    data = response.json()
    logger.info(f"{len(data)} produtos extraídos com sucesso.")

    return data