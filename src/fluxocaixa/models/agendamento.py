# src/fluxocaixa/models/agendamento.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Text,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .base import Base


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String(100), nullable=False)
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=True)
    procedimento = Column(String(100), nullable=False)

    pagamento = Column(String(50), nullable=True)
    valor_servico = Column(Float, nullable=True, default=0)
    valor_sinal = Column(Float, nullable=True, default=0)
    observacoes = Column(Text, nullable=True)

    status = Column(String(50), nullable=True, default="Pendente")

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    empresa = relationship("Empresa", back_populates="agendamentos")

    servico = relationship("Servico", back_populates="agendamentos")

    def to_dict(self):
        preco_servico = self.valor_servico or (self.servico.valor if self.servico else 0)
        falta_pagar = preco_servico - (self.valor_sinal or 0)

        return {
            "id": self.id,
            "cliente": self.cliente,
            "data": self.data.strftime("%Y-%m-%d") if self.data else "",
            "hora": self.hora.strftime("%H:%M") if self.hora else "",
            "procedimento": self.procedimento,
            "pagamento": self.pagamento or "",
            "valor_servico": float(preco_servico),
            "valor_sinal": float(self.valor_sinal or 0),
            "falta_pagar": max(float(falta_pagar), 0),
            "observacoes": self.observacoes or "",
            "status": self.status or "Pendente",
        }
