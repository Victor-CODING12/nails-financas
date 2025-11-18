# src/fluxocaixa/models/servico.py

from sqlalchemy import Column, Integer, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    valor = Column(Float, nullable=False)
    duracao = Column(Integer, nullable=False)
    descricao = Column(String(255))

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="servicos")

    agendamentos = relationship("Agendamento", back_populates="servico")
