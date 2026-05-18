# API Price Pipeline

ETL pipeline that extracts product data from a public e-commerce API, transforms it with Pandas, persists it in PostgreSQL, and visualizes it in a Streamlit dashboard.

---

## Stack

| Layer | Technology |
|---|---|
| Extraction | Python + Requests |
| Transformation | Pandas |
| Database | PostgreSQL (Neon) |
| ORM / Queries | SQLAlchemy |
| Dashboard | Streamlit + Plotly |
| Environment | GitHub Codespaces |

---

## Project Structure

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
│       └── products.json    # Local data file (dev environment)
│
├── streamlit_app.py         # Dashboard entry point
├── requirements.txt
└── .env                     # Not versioned — see .env.example
```

---

## Data Source

**Fake Store API** — `https://fakestoreapi.com/products`

Public API, no authentication required. Returns 20 products with: `id`, `title`, `price`, `category`, `description`, `image`, `rating`.

> **Note:** In GitHub Codespaces, the API is blocked by Cloudflare. Raw data is loaded from `data/raw/products.json` instead. To fetch live data, download the JSON from the URL above and save it to that path.

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/api_price_pipeline.git
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
DATABASE_URL=postgresql+psycopg2://user:password@host/dbname?sslmode=require
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

## Dashboard

Four sections powered by direct SQL queries against PostgreSQL:

- **Overview** — total products, categories, average price, top-rated product
- **Average price by category** — bar chart
- **Price range by category** — grouped bar chart (min vs max)
- **Top 5 rated products** — sortable table
- **Product explorer** — full table with category filter

---

## Pipeline Architecture

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

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DATABASE_URL` | ✅ | — | PostgreSQL connection string |
| `API_URL` | ❌ | `https://fakestoreapi.com/products` | API endpoint |
| `LOG_LEVEL` | ❌ | `INFO` | Logging verbosity |# api_price_pipelane
