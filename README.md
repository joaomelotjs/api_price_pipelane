# API Price Pipeline

ETL pipeline that extracts product data from a public e-commerce API, transforms it with Pandas, persists it in PostgreSQL, and visualizes it in an interactive Streamlit dashboard.

Built as a portfolio project to practice real-world data engineering — with a focus on clean architecture, modular code, and professional organization.

🔗 [View the live dashboard](https://apipricepipelane-9ympwvtp5eh8rst39sebvc.streamlit.app/)

---

## About the project

The API Price Pipeline extracts product data from a public e-commerce API, applies transformations, persists the results in a cloud PostgreSQL database, and presents them through an interactive dashboard.

This project was developed as part of my data engineering learning process, with the goal of building an organized, modular, and technically consistent application — close to a real professional environment.

---

## Stack

| Layer | Technology |
|---|---|
| Extraction | Python + Requests |
| Transformation | Pandas |
| Database | PostgreSQL (Neon) |
| ORM | SQLAlchemy + pg8000 |
| Dashboard | Streamlit + Plotly |
| Dev environment | GitHub Codespaces |
| Deploy | Streamlit Cloud |

---

## Project structure

```
api_price_pipeline/
│
├── app/
│   ├── pipeline/
│   │   ├── extract.py       # Fetch raw data from API or local file
│   │   ├── transform.py     # Clean and structure with Pandas
│   │   ├── load.py          # Persist to PostgreSQL
│   │   └── pipeline.py      # Orchestrates extract → transform → load
│   │
│   ├── database/
│   │   ├── connection.py    # SQLAlchemy engine and session management
│   │   ├── models.py        # ORM table definitions
│   │   └── queries.py       # Reusable queries for the dashboard
│   │
│   └── config/
│       └── settings.py      # Reads and validates .env variables
│
├── data/
│   └── raw/
│       └── products.json    # Local data file (dev environment fallback)
│
├── tests/
│   ├── test_extract.py      # Unit tests for extraction module
│   └── test_transform.py    # Unit tests for transformation module
│
├── streamlit_app.py         # Dashboard entry point
├── Dockerfile               # Containerizes the ETL pipeline
├── docker-compose.yml       # Runs the pipeline in a container
├── requirements.txt
└── .env                     # Not versioned — see .env.example
```

---

## Pipeline architecture

```
Fake Store API / local JSON
        ↓
   extract.py       → list[dict]  (raw data, no transformation)
        ↓
  transform.py      → pd.DataFrame (clean, typed, rating extracted)
        ↓
    load.py         → PostgreSQL via SQLAlchemy (bulk insert)
        ↓
   queries.py       → analytical queries for the dashboard
        ↓
streamlit_app.py    → Streamlit + Plotly visualization
```

---

## Dashboard

Four sections powered by direct SQL queries against PostgreSQL:

- **Overview** — total products, categories, average price, top-rated product
- **Average price by category** — bar chart
- **Price range by category** — grouped bar chart (min vs max)
- **Top 5 rated products** — sortable table
- **Product explorer** — full table with category filter

---

## Data source

**Fake Store API** — `https://fakestoreapi.com/products`

Public API, no authentication required. Returns 20 products with: `id`, `title`, `price`, `category`, `description`, `image`, `rating`.

> **Note:** In GitHub Codespaces, the API is blocked by Cloudflare. Raw data is loaded from `data/raw/products.json` instead. To fetch live data, download the JSON from the URL above and save it to that path.

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/joaomelotjs/api_price_pipeline.git
cd api_price_pipeline
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` with your Neon connection string:
```env
DATABASE_URL=postgresql+pg8000://user:password@host/dbname?sslmode=require
API_URL=https://fakestoreapi.com/products
LOG_LEVEL=INFO
```

**4. Create the database table**
```bash
python -c "from app.database.models import create_tables; create_tables()"
```

**5. Run the pipeline**
```bash
python -m app.pipeline.pipeline
```

**6. Launch the dashboard**
```bash
streamlit run streamlit_app.py
```

---

## Docker

The ETL pipeline can be run in a container — no local Python setup required.

**Build the image**
```bash
docker build -t api-price-pipeline .
```

**Run the pipeline**
```bash
docker run --env-file .env api-price-pipeline
```

**Or with docker compose**
```bash
docker compose up
```

> The database (Neon) and dashboard (Streamlit Cloud) run outside the container. Docker is used only to containerize and run the ETL pipeline in an isolated, reproducible environment.

---

## Deploy (Streamlit Cloud)

1. Push the repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account
3. Click **New app** and fill in:
   - **Repository:** `joaomelotjs/api_price_pipeline`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **Advanced settings → Secrets** and add:
```
DATABASE_URL = "postgresql+pg8000://user:password@host/dbname?sslmode=require"
```
5. Set **Python version** to `3.12`
6. Click **Deploy**

> The dashboard reads data directly from PostgreSQL — no need to run the pipeline on the cloud. Run `python -m app.pipeline.pipeline` locally whenever you want to refresh the data.

---

## Tests

Unit tests cover the extraction and transformation modules.

**Run all tests**
```bash
pytest tests/ -v
```

**Coverage**
- `test_extract.py` — local file loading, data structure, error handling
- `test_transform.py` — rating unnesting, expected columns, data types, null handling

---

## Technical decisions

**pg8000 instead of psycopg2**
psycopg2 is incompatible with Python 3.14 on Streamlit Cloud. pg8000 is a pure Python driver with no native dependencies, and resolves the issue without compromising functionality.

**SSL via connect_args**
SSL configuration with Neon was done via `connect_args={"ssl_context": True}` in SQLAlchemy — the correct format for pg8000.

**Local fallback in extract.py**
The Fake Store API blocks requests from GitHub Codespaces via Cloudflare. In development, the pipeline reads from `data/raw/products.json`. In production, extraction happens directly via the REST API.

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | ✅ | — | PostgreSQL connection string |
| `API_URL` | ❌ | `https://fakestoreapi.com/products` | API endpoint |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity |

---

## About this project

This project was developed as part of my practical learning in data engineering. The goal was to build a real ETL pipeline — with justified technical decisions, modular architecture, and functional deploy — as a foundation for my portfolio in the field.

Technologies, architectural decisions, and limitations encountered along the way were documented throughout development to reflect an organized and professional working process.

---

## Author

**João Pedro Melo**
[github.com/joaomelotjs](https://github.com/joaomelotjs)