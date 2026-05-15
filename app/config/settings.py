"""
settings.py
-----------
Lê e valida variáveis de ambiente usando pydantic-settings.

Por que pydantic-settings e não python-dotenv puro?
  - Valida tipos em tempo de inicialização (falha rápido se algo estiver errado)
  - Documenta as variáveis obrigatórias de forma explícita no código
  - Integra bem com o restante do ecossistema Python moderno

Variáveis esperadas no .env:
  DATABASE_URL  — connection string do Neon (obrigatória)
  API_URL       — endpoint da Fake Store API (tem default)
  LOG_LEVEL     — nível de logging (tem default)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Banco de dados ---
    # Formato esperado: postgresql+psycopg2://user:password@host/dbname?sslmode=require
    DATABASE_URL: str

    # --- API externa ---
    API_URL: str = "https://fakestoreapi.com/products"

    # --- Controle de execução ---
    LOG_LEVEL: str = "INFO"

    # Pydantic vai procurar o arquivo .env na raiz do projeto.
    # env_file_encoding garante compatibilidade em Windows/Linux.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Instância global — importar de outros módulos com:
#   from app.config.settings import settings
settings = Settings()