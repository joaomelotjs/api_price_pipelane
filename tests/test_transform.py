"""
test_transform.py
-----------------
Testes unitários para app/pipeline/transform.py

Estratégia: dados sintéticos criados no próprio teste.
Sem dependência de arquivo local, banco ou API.

Cobertura:
  - Desaninhamento do campo rating
  - Presença das colunas esperadas no DataFrame resultante
  - Tipos corretos das colunas
  - Remoção de linhas com campos obrigatórios nulos
"""

import pandas as pd
import pytest

from app.pipeline.transform import transform_products


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_raw_data():
    """Dados brutos simulando o retorno da Fake Store API."""
    return [
        {
            "id": 1,
            "title": "Product A",
            "price": 29.99,
            "category": "electronics",
            "description": "A great product",
            "image": "https://example.com/image1.png",
            "rating": {"rate": 4.5, "count": 120},
        },
        {
            "id": 2,
            "title": "Product B",
            "price": 9.99,
            "category": "clothing",
            "description": "Another product",
            "image": "https://example.com/image2.png",
            "rating": {"rate": 3.8, "count": 45},
        },
    ]


@pytest.fixture
def transformed_df(sample_raw_data):
    """DataFrame já transformado — reutilizado em vários testes."""
    return transform_products(sample_raw_data)


# ── Testes de colunas ─────────────────────────────────────────────────────────

def test_colunas_esperadas_existem(transformed_df):
    """Todas as colunas esperadas devem estar presentes no DataFrame."""
    expected_columns = {
        "id", "title", "price", "category",
        "description", "image", "rating_rate", "rating_count"
    }
    assert expected_columns.issubset(set(transformed_df.columns))


def test_coluna_rating_original_removida(transformed_df):
    """A coluna rating aninhada original não deve existir no resultado."""
    assert "rating" not in transformed_df.columns


# ── Testes de desaninhamento ──────────────────────────────────────────────────

def test_rating_rate_extraido_corretamente(transformed_df):
    """rating_rate deve conter os valores extraídos do dicionário aninhado."""
    assert transformed_df["rating_rate"].iloc[0] == 4.5
    assert transformed_df["rating_rate"].iloc[1] == 3.8


def test_rating_count_extraido_corretamente(transformed_df):
    """rating_count deve conter os valores extraídos do dicionário aninhado."""
    assert transformed_df["rating_count"].iloc[0] == 120
    assert transformed_df["rating_count"].iloc[1] == 45


# ── Testes de tipos ───────────────────────────────────────────────────────────

def test_tipos_corretos(transformed_df):
    """As colunas devem ter os tipos corretos após a transformação."""
    assert transformed_df["id"].dtype == int
    assert transformed_df["price"].dtype == float
    assert transformed_df["rating_rate"].dtype == float


# ── Testes de limpeza ─────────────────────────────────────────────────────────

def test_remove_linhas_com_campos_obrigatorios_nulos():
    """Linhas com title, price ou category nulos devem ser removidas."""
    raw_data_com_nulo = [
        {
            "id": 1,
            "title": None,  # campo obrigatório nulo
            "price": 10.0,
            "category": "electronics",
            "description": "desc",
            "image": "img.png",
            "rating": {"rate": 4.0, "count": 10},
        },
        {
            "id": 2,
            "title": "Valid Product",
            "price": 20.0,
            "category": "clothing",
            "description": "desc",
            "image": "img.png",
            "rating": {"rate": 3.5, "count": 5},
        },
    ]
    df = transform_products(raw_data_com_nulo)
    assert len(df) == 1
    assert df["title"].iloc[0] == "Valid Product"


def test_quantidade_correta_de_produtos(transformed_df, sample_raw_data):
    """O número de produtos transformados deve ser igual ao de entrada."""
    assert len(transformed_df) == len(sample_raw_data)