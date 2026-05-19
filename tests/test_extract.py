"""
test_extract.py
---------------
Testes unitários para app/pipeline/extract.py

Estratégia: usa tmp_path do pytest para criar arquivos temporários.
Sem dependência do arquivo real em data/raw/ ou da API externa.

Cobertura:
  - Carregamento correto do arquivo JSON local
  - Estrutura dos dados retornados (list[dict])
  - Campos esperados em cada produto
  - Erro quando arquivo não existe
  - Erro quando source é inválido
"""

import json
import pytest

from app.pipeline.extract import fetch_products


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_products():
    """Lista de produtos simulando o conteúdo do products.json."""
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
def local_json_file(tmp_path, sample_products, monkeypatch):
    """
    Cria um arquivo JSON temporário e redireciona LOCAL_FILE para ele.

    tmp_path: pasta temporária criada e apagada automaticamente pelo pytest.
    monkeypatch: substitui a constante LOCAL_FILE durante o teste.
    """
    json_file = tmp_path / "products.json"
    json_file.write_text(json.dumps(sample_products), encoding="utf-8")

    # Redireciona o módulo para usar o arquivo temporário
    import app.pipeline.extract as extract_module
    monkeypatch.setattr(extract_module, "LOCAL_FILE", str(json_file))

    return json_file


# ── Testes de carregamento ────────────────────────────────────────────────────

def test_carrega_arquivo_local_com_sucesso(local_json_file, sample_products):
    """fetch_products() deve retornar a lista correta do arquivo local."""
    result = fetch_products(source="file")
    assert result == sample_products


def test_retorna_lista(local_json_file):
    """O retorno deve ser uma lista."""
    result = fetch_products(source="file")
    assert isinstance(result, list)


def test_retorna_lista_de_dicionarios(local_json_file):
    """Cada item da lista deve ser um dicionário."""
    result = fetch_products(source="file")
    assert all(isinstance(item, dict) for item in result)


def test_quantidade_correta_de_produtos(local_json_file, sample_products):
    """O número de produtos retornados deve ser igual ao do arquivo."""
    result = fetch_products(source="file")
    assert len(result) == len(sample_products)


def test_campos_esperados_presentes(local_json_file):
    """Cada produto deve conter os campos esperados da API."""
    result = fetch_products(source="file")
    expected_fields = {"id", "title", "price", "category", "description", "image", "rating"}
    for product in result:
        assert expected_fields.issubset(set(product.keys()))


# ── Testes de erro ────────────────────────────────────────────────────────────

def test_erro_quando_arquivo_nao_existe(monkeypatch):
    """Deve lançar RuntimeError quando o arquivo local não existe."""
    import app.pipeline.extract as extract_module
    monkeypatch.setattr(extract_module, "LOCAL_FILE", "/caminho/inexistente/products.json")

    with pytest.raises(RuntimeError, match="Arquivo não encontrado"):
        fetch_products(source="file")


def test_erro_quando_source_invalido(local_json_file):
    """Deve lançar ValueError quando source não é 'file' nem 'api'."""
    with pytest.raises(ValueError, match="source inválido"):
        fetch_products(source="invalido")