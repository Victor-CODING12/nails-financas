# src/fluxocaixa/models/fluxo_caixa.py

from sqlalchemy import Column, Integer, String, Float, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class FluxoCaixa(Base):
    __tablename__ = "fluxo_caixa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(10), nullable=False)  # 'entrada' ou 'saida'
    data = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String(255), nullable=True)
    categoria = Column(String(100), nullable=True)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="fluxos_caixa")

    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "data": self.data.strftime("%Y-%m-%d") if self.data else "",
            "valor": self.valor,
            "descricao": self.descricao or "",
            "categoria": self.categoria or "",
        }
