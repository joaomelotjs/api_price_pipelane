"""
pipeline.py
-----------
Ponto de entrada do ETL. Orquestra as três etapas em sequência:
  1. extract  — busca dados brutos
  2. transform — limpa e estrutura
  3. load     — persiste no banco

Como executar:
  python -m app.pipeline.pipeline

Por que usar logging e não print?
  logging permite controlar o nível de verbosidade via LOG_LEVEL no .env
  e é o padrão para aplicações que vão para produção.
"""

import logging
import sys
from datetime import datetime, timezone

from app.pipeline.extract import fetch_products
from app.pipeline.transform import transform_products
from app.pipeline.load import load_products
from app.config.settings import settings

# Configuração de logging baseada no .env
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def run_pipeline(source: str = "file") -> None:
    """
    Executa o pipeline ETL completo.

    Parâmetros:
        source: "file" usa arquivo local (dev)
                "api"  chama a Fake Store API (produção)
    """
    start = datetime.now(timezone.utc)
    logger.info("=" * 50)
    logger.info("Iniciando pipeline ETL")
    logger.info(f"Source: {source}")
    logger.info("=" * 50)

    try:
        # Extract
        logger.info("Etapa 1/3 — Extract")
        raw_data = fetch_products(source=source)

        # Transform
        logger.info("Etapa 2/3 — Transform")
        df = transform_products(raw_data)

        # Load
        logger.info("Etapa 3/3 — Load")
        load_products(df)

        elapsed = (datetime.now(timezone.utc) - start).total_seconds()
        logger.info(f"Pipeline concluído em {elapsed:.2f}s")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Pipeline falhou: {e}")
        logger.info("=" * 50)
        sys.exit(1)


if __name__ == "__main__":
    run_pipeline()