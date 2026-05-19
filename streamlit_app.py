"""
streamlit_app.py
----------------
Ponto de entrada do dashboard — fica na raiz do projeto para que
o Streamlit resolva os imports do pacote app corretamente.

Como executar:
  streamlit run streamlit_app.py
"""

import streamlit as st
import plotly.express as px
import os
st.write("DATABASE_URL prefix:", os.environ.get("DATABASE_URL", "NÃO ENCONTRADA")[:30])

from app.database.queries import (
    get_all_products,
    get_avg_price_by_category,
    get_price_range_by_category,
    get_top_rated_products,
)
from app.pipeline.pipeline import run_pipeline

# ── Configuração da página ───────────────────────────────────────────────────

st.set_page_config(
    page_title="API Price Pipeline",
    page_icon="📦",
    layout="wide",
)

# ── Estilos customizados ─────────────────────────────────────────────────────

st.markdown("""
<style>
    .metric-card {
        background-color: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #313244;
    }
    .metric-label {
        color: #a6adc8;
        font-size: 13px;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #cdd6f4;
        font-size: 28px;
        font-weight: 700;
    }
    .metric-sub {
        color: #89b4fa;
        font-size: 12px;
        margin-top: 4px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        color: #cdd6f4;
        margin-bottom: 4px;
    }
    .divider {
        border-top: 1px solid #313244;
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────

col_title, col_btn = st.columns([5, 1])

with col_title:
    st.title("📦 API Price Pipeline")
    st.caption("Dashboard de análise de produtos — Fake Store API → PostgreSQL")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Atualizar dados", use_container_width=True):
        with st.spinner("Rodando pipeline ETL..."):
            run_pipeline()
        st.success("Pipeline concluído!")
        st.rerun()

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Carrega dados ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_data():
    return {
        "all":       get_all_products(),
        "avg_price": get_avg_price_by_category(),
        "range":     get_price_range_by_category(),
        "top":       get_top_rated_products(limit=5),
    }

data = load_data()
df_all   = data["all"]
df_avg   = data["avg_price"]
df_range = data["range"]
df_top   = data["top"]

# ── Seção 1: Métricas gerais ─────────────────────────────────────────────────

st.markdown('<div class="section-title">Visão Geral</div>', unsafe_allow_html=True)
st.markdown("")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total de Produtos</div>
        <div class="metric-value">{len(df_all)}</div>
        <div class="metric-sub">da Fake Store API</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Categorias</div>
        <div class="metric-value">{df_all['category'].nunique()}</div>
        <div class="metric-sub">categorias distintas</div>
    </div>""", unsafe_allow_html=True)

with c3:
    avg = df_all['price'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Preço Médio Geral</div>
        <div class="metric-value">$ {avg:.2f}</div>
        <div class="metric-sub">todos os produtos</div>
    </div>""", unsafe_allow_html=True)

with c4:
    top_rated = df_all.loc[df_all['rating_rate'].idxmax()]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Melhor Avaliado</div>
        <div class="metric-value">⭐ {top_rated['rating_rate']}</div>
        <div class="metric-sub">{top_rated['title'][:30]}...</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Seção 2: Preço médio por categoria ───────────────────────────────────────

st.markdown('<div class="section-title">Preço Médio por Categoria</div>', unsafe_allow_html=True)
st.markdown("")

fig_avg = px.bar(
    df_avg,
    x="category",
    y="avg_price",
    color="category",
    text="avg_price",
    labels={"category": "Categoria", "avg_price": "Preço Médio (USD)"},
    color_discrete_sequence=px.colors.qualitative.Pastel,
)
fig_avg.update_traces(texttemplate="$ %{text:.2f}", textposition="outside")
fig_avg.update_layout(
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#cdd6f4",
    yaxis=dict(gridcolor="#313244"),
    xaxis=dict(gridcolor="#313244"),
    margin=dict(t=20),
)
st.plotly_chart(fig_avg, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Seção 3: Range de preços por categoria ───────────────────────────────────

st.markdown('<div class="section-title">Range de Preços por Categoria</div>', unsafe_allow_html=True)
st.markdown("")

df_range_melted = df_range.melt(
    id_vars="category",
    value_vars=["min_price", "max_price"],
    var_name="tipo",
    value_name="preco",
)
df_range_melted["tipo"] = df_range_melted["tipo"].map({
    "min_price": "Menor Preço",
    "max_price": "Maior Preço",
})

fig_range = px.bar(
    df_range_melted,
    x="category",
    y="preco",
    color="tipo",
    barmode="group",
    labels={"category": "Categoria", "preco": "Preço (USD)", "tipo": ""},
    color_discrete_map={"Menor Preço": "#89b4fa", "Maior Preço": "#f38ba8"},
)
fig_range.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#cdd6f4",
    yaxis=dict(gridcolor="#313244"),
    xaxis=dict(gridcolor="#313244"),
    margin=dict(t=20),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
st.plotly_chart(fig_range, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Seção 4: Top 5 produtos avaliados ────────────────────────────────────────

st.markdown('<div class="section-title">Top 5 Produtos Mais Bem Avaliados</div>', unsafe_allow_html=True)
st.markdown("")

df_top_display = df_top.copy()
df_top_display["rating_rate"] = df_top_display["rating_rate"].apply(lambda x: f"⭐ {x}")
df_top_display["price"] = df_top_display["price"].apply(lambda x: f"$ {x:.2f}")
df_top_display.columns = ["ID", "Produto", "Categoria", "Preço", "Avaliação", "Nº Avaliações"]

st.dataframe(df_top_display, use_container_width=True, hide_index=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Seção 5: Explorador de produtos ──────────────────────────────────────────

st.markdown('<div class="section-title">Explorador de Produtos</div>', unsafe_allow_html=True)
st.markdown("")

categorias = ["Todas"] + sorted(df_all["category"].unique().tolist())
categoria_selecionada = st.selectbox("Filtrar por categoria", categorias)

df_filtrado = df_all if categoria_selecionada == "Todas" else df_all[df_all["category"] == categoria_selecionada]

df_exibir = df_filtrado[["title", "category", "price", "rating_rate", "rating_count"]].copy()
df_exibir.columns = ["Produto", "Categoria", "Preço (USD)", "Avaliação", "Nº Avaliações"]

st.dataframe(df_exibir, use_container_width=True, hide_index=True)
st.caption(f"{len(df_filtrado)} produto(s) exibido(s)")