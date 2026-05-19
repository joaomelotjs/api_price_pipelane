"""
connection.py
-------------
Gerencia a conexão com o banco PostgreSQL (Neon) via SQLAlchemy.

Expõe dois objetos para uso nos outros módulos:
  - engine        → usado em models.py (DDL) e load.py (bulk insert com pandas)
  - SessionLocal  → usado em queries.py (consultas ORM)
  - get_session   → context manager seguro para abrir/fechar sessões

Por que pool_pre_ping=True?
  O Neon (serverless Postgres) fecha conexões ociosas agressivamente.
  pool_pre_ping faz um SELECT 1 antes de reutilizar uma conexão do pool,
  descartando conexões mortas silenciosamente em vez de explodir com erro.

Por que pool_size=5 e max_overflow=10?
  Valores conservadores adequados para um pipeline ETL com baixa concorrência.
  Evita abrir conexões desnecessárias no plano gratuito do Neon.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from app.config.settings import settings

# Garante compatibilidade com pg8000 no Streamlit Cloud
db_url = settings.DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+pg8000://")
db_url = db_url.replace("postgresql://", "postgresql+pg8000://")
db_url = db_url.replace("?sslmode=require", "")  # pg8000 trata SSL diferente


# Engine principal — reutilizado em todo o projeto
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False,
    connect_args={"ssl_context": True},  # SSL para pg8000
)


# Fábrica de sessões ORM
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # controle manual de transações
    autoflush=False,   # não faz flush automático antes de queries
)


@contextmanager
def get_session() -> Session:
    """
    Context manager que garante abertura e fechamento correto da sessão.

    Uso:
        with get_session() as session:
            session.execute(...)

    Em caso de exceção, o rollback é feito automaticamente.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def test_connection() -> bool:
    """
    Verifica se a conexão com o banco está funcionando.
    Útil para checar no startup ou em scripts de diagnóstico.

    Retorna True se OK, propaga a exceção se falhar.
    """
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True