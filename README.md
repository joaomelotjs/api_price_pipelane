# API Price Pipeline

Pipeline ETL de dados de e-commerce construído com Python, PostgreSQL e Streamlit.

---

## Sobre o projeto

O API Price Pipeline é um pipeline de dados que extrai informações de produtos de uma API pública de e-commerce, transforma e persiste em um banco de dados relacional, e apresenta os resultados em um dashboard interativo.

O projeto foi desenvolvido como parte do meu processo de aprendizado em engenharia de dados, com foco em construir uma aplicação organizada, modular e tecnicamente consistente — próxima de um ambiente profissional real.

---

## Funcionalidades

- Extração de dados via API REST (Fake Store API)
- Fallback para arquivo local em ambientes com restrições de rede
- Transformação e limpeza dos dados com Pandas
- Persistência em banco PostgreSQL na nuvem (Neon)
- Dashboard interativo com Streamlit e Plotly
- Deploy em nuvem via Streamlit Cloud

---

## Stack

| Camada | Tecnologia |
|---|---|
| Extração | Python + Requests |
| Transformação | Pandas |
| Banco de dados | PostgreSQL (Neon) |
| ORM | SQLAlchemy + pg8000 |
| Dashboard | Streamlit + Plotly |
| Ambiente de desenvolvimento | GitHub Codespaces |
| Deploy | Streamlit Cloud |

---

## Arquitetura

```
api_price_pipeline/
│
├── app/
│   ├── pipeline/
│   │   ├── extract.py       # Extração via API ou arquivo local
│   │   ├── transform.py     # Limpeza e transformação com Pandas
│   │   ├── load.py          # Persistência no PostgreSQL
│   │   └── pipeline.py      # Orquestração do fluxo ETL
│   │
│   ├── database/
│   │   ├── connection.py    # Conexão com o banco via SQLAlchemy
│   │   ├── models.py        # Definição das tabelas
│   │   └── queries.py       # Consultas reutilizáveis
│   │
│   └── config/
│       └── settings.py      # Variáveis de ambiente
│
├── data/
│   └── raw/                 # Dados brutos para fallback local
│
├── streamlit_app.py         # Ponto de entrada do dashboard
├── requirements.txt
└── .gitignore
```

---

## Fluxo ETL

```
Fake Store API
      ↓
  extract.py
      ↓
 transform.py
      ↓
   load.py
      ↓
PostgreSQL (Neon)
      ↓
 streamlit_app.py
```

---

## Dashboard

O dashboard apresenta quatro seções:

- **Visão Geral** — métricas gerais do catálogo de produtos
- **Preço médio por categoria** — comparativo entre categorias
- **Range de preços** — distribuição de preços dos produtos
- **Top avaliados** — produtos com melhor avaliação

---

## Decisões técnicas

**Driver pg8000 no lugar de psycopg2**
O psycopg2 apresenta incompatibilidade com Python 3.14 no Streamlit Cloud. O pg8000 é um driver puro Python, sem dependências nativas, e resolve o problema sem comprometer a funcionalidade.

**SSL via connect_args**
A configuração de SSL com Neon foi feita via `connect_args={"ssl_context": True}` no SQLAlchemy, que é o formato correto para o pg8000.

**Fallback local no extract.py**
A Fake Store API bloqueia requisições vindas do GitHub Codespaces via Cloudflare. Em desenvolvimento, o pipeline lê de `data/raw/products.json`. Em produção, a extração ocorre diretamente via API REST.

---

## Como executar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/api_price_pipeline.git
cd api_price_pipeline
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz com:
```
DATABASE_URL=postgresql+pg8000://user:password@host.neon.tech/dbname
```

**4. Execute o pipeline**
```bash
python -m app.pipeline.pipeline
```

**5. Inicie o dashboard**
```bash
streamlit run streamlit_app.py
```

---

## Sobre o desenvolvimento

Este projeto foi desenvolvido como parte do meu aprendizado prático em engenharia de dados. O objetivo foi construir um pipeline ETL real — com decisões técnicas justificadas, arquitetura modular e deploy funcional — como base para meu portfólio na área.

Tecnologias, decisões de arquitetura e limitações encontradas foram documentadas ao longo do desenvolvimento para refletir um processo de trabalho organizado e profissional.

---

## Autor

João Pedro Melo
[github.com/joaomelotjs](https://github.com/joaomelotjs)
