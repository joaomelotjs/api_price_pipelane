"""
extract.py
----------
Responsabilidade única: buscar dados brutos da Fake Store API.

Não transforma, não limpa, não persiste.
Retorna os dados exatamente como a API entrega — lista de dicionários.

Nota de ambiente:
  Em desenvolvimento (Codespace), a Fake Store API é bloqueada pelo Cloudflare.
  Por isso, fetch_products() lê de data/raw/products.json por padrão.
  Em produção, trocar source="file" para source="api".

Por que retornar lista de dicionários e não DataFrame?
  Manter a separação clara entre camadas:
  - extract  → dados brutos (list[dict])
  - transform → dados limpos (DataFrame)
  - load     → persistência (PostgreSQL)
"""

import json
import logging
import os

import requests

from app.config.settings import settings

logger = logging.getLogger(__name__)

# Caminho do arquivo local relativo à raiz do projeto
LOCAL_FILE = os.path.join("data", "raw", "products.json")


def fetch_products(source: str = "file") -> list[dict]:
    """
    Retorna lista de produtos brutos.

    Parâmetros:
        source: "file" lê do arquivo local (dev)
                "api"  chama a Fake Store API (produção)

    Retorna:
        list[dict] com os campos: id, title, price, category, description, image, rating

    Lança:
        RuntimeError — se arquivo não encontrado ou API retornar erro
    """
    if source == "file":
        return _fetch_from_file()
    elif source == "api":
        return _fetch_from_api()
    else:
        raise ValueError(f"source inválido: '{source}'. Use 'file' ou 'api'.")


def _fetch_from_file() -> list[dict]:
    """Lê produtos do arquivo JSON local."""
    if not os.path.exists(LOCAL_FILE):
        raise RuntimeError(
            f"Arquivo não encontrado: {LOCAL_FILE}\n"
            "Baixe os dados em https://fakestoreapi.com/products e salve em data/raw/products.json"
        )

    with open(LOCAL_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"{len(data)} produtos carregados de {LOCAL_FILE}.")
    return data


def _fetch_from_api() -> list[dict]:
    """Chama a Fake Store API diretamente."""
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