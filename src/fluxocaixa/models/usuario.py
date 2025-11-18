# src/fluxocaixa/models/usuario.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    # Dados principais
    nome = Column(String(150), nullable=False)
    cnpj = Column(String(20), unique=True, nullable=True)
    email = Column(String(150), unique=True, nullable=False)

    # 📞 Novo campo: Telefone/WhatsApp
    telefone = Column(String(20), nullable=True)

    # 📅 Novo campo: dias de funcionamento (lista em string: "seg,ter,qua")
    dias_funcionamento = Column(String(50), nullable=True)

    # ⏰ Novo campo: horários
    hora_abre = Column(String(5), nullable=True)   # ex.: "08:00"
    hora_fecha = Column(String(5), nullable=True)  # ex.: "18:00"

    # Relacionamentos
    usuarios = relationship("Usuario", back_populates="empresa")
    fluxos_caixa = relationship("FluxoCaixa", back_populates="empresa")
    agendamentos = relationship("Agendamento", back_populates="empresa")
    servicos = relationship("Servico", back_populates="empresa")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    empresa = relationship("Empresa", back_populates="usuarios")
