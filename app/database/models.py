from datetime import datetime
 
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
 
 
class Base(DeclarativeBase):
    """Base para todos os modelos do projeto."""
    pass
 
 
class Product(Base):
    __tablename__ = "products"
 
    # Chave primária — mesmo id que vem da API
    id = Column(Integer, primary_key=True, index=True)
 
    # Campos da API
    title       = Column(String(500), nullable=False)
    price       = Column(Float, nullable=False)
    category    = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    image       = Column(String(1000), nullable=True)
    rating_rate  = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
 
    # Campos de controle do pipeline
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
 
    def __repr__(self):
        return f"<Product id={self.id} title='{self.title[:30]}' price={self.price}>"
 
 
def create_tables() -> None:
    """
    Cria todas as tabelas no banco se ainda não existirem.
    Seguro para rodar múltiplas vezes — não apaga dados existentes.
 
    Chamado em pipeline.py antes de carregar os dados.
    """
    from app.database.connection import engine
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas (ou já existiam).")