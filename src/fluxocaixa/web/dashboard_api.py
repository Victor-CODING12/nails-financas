from fastapi import APIRouter
from datetime import date, timedelta
from sqlalchemy import func
from ..models import db, Agendamento
from ..models.fluxo_caixa import FluxoCaixa

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("")
def obter_dados_dashboard():
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=6)

    # ===== 1️⃣ FATURAMENTO BRUTO (somente entradas) =====
    total_bruto = (
        db.session.query(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "entrada")
        .scalar()
        or 0
    )

    # ===== 2️⃣ DESPESAS / SAÍDAS =====
    total_saidas = (
        db.session.query(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "saida")
        .scalar()
        or 0
    )

    # ===== 3️⃣ LUCRO LÍQUIDO =====
    total_liquido = total_bruto - total_saidas

    # ===== 4️⃣ QTD DE VENDAS E TICKET MÉDIO =====
    qtd_vendas = (
        db.session.query(func.count(FluxoCaixa.id))
        .filter(FluxoCaixa.tipo == "entrada")
        .scalar()
        or 0
    )
    ticket_medio = total_bruto / qtd_vendas if qtd_vendas > 0 else 0

    # ===== 5️⃣ FATURAMENTO DIÁRIO (últimos 7 dias) =====
    vendas_dia = (
        db.session.query(
            func.date(FluxoCaixa.data).label("data"),
            func.sum(FluxoCaixa.valor).label("valor")
        )
        .filter(
            FluxoCaixa.tipo == "entrada",
            FluxoCaixa.data >= inicio_semana
        )
        .group_by(func.date(FluxoCaixa.data))
        .order_by(func.date(FluxoCaixa.data))
        .all()
    )
    grafico_faturamento = [
        {"data": v.data.strftime("%d/%m"), "valor": float(v.valor)} for v in vendas_dia
    ]

    # ===== 6️⃣ SERVIÇOS MAIS VENDIDOS (últimos 7 dias) =====
    servicos_mais_vendidos = (
        db.session.query(
            Agendamento.procedimento.label("nome"),
            func.count(Agendamento.id).label("total")
        )
        .filter(Agendamento.data >= inicio_semana)
        .group_by(Agendamento.procedimento)
        .order_by(func.count(Agendamento.id).desc())
        .limit(5)
        .all()
    )
    grafico_servicos = [{"nome": s.nome, "total": int(s.total)} for s in servicos_mais_vendidos]

    # ===== 7️⃣ RETORNO FINAL =====
    return {
        "total_bruto": float(total_bruto),
        "total_liquido": float(total_liquido),
        "qtd_vendas": int(qtd_vendas),
        "ticket_medio": round(float(ticket_medio), 2),
        "grafico_faturamento": grafico_faturamento,
        "grafico_servicos": grafico_servicos
    }