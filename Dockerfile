# Dockerfile
# ----------
# Containeriza o pipeline ETL da aplicação.
# O banco (Neon) e o dashboard (Streamlit Cloud) ficam fora do container.
#
# Como usar:
#   docker build -t api-price-pipeline .
#   docker run --env-file .env api-price-pipeline

FROM python:3.12-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala dependências primeiro (camada cacheável)
# Se requirements.txt não mudar, o Docker reutiliza esta camada
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY app/ ./app/
COPY data/ ./data/

# Variáveis de ambiente com defaults seguros
ENV LOG_LEVEL=INFO
ENV API_URL=https://fakestoreapi.com/products

# Comando padrão: roda o pipeline ETL
CMD ["python", "-m", "app.pipeline.pipeline"]