from fastapi import Request, Depends
from sqlalchemy import func
from . import router, templates
from ..auth.current_user_web import usuario_atual_web
from ..models import FluxoCaixa, Agendamento, Servico


# =======================================
#  📊 PÁGINA PRINCIPAL DOS RELATÓRIOS
# =======================================

@router.get("/relatorios")
async def relatorios(request: Request, usuario=Depends(usuario_atual_web)):
    # Resumo financeiro
    total_entradas = (
        FluxoCaixa.query.with_entities(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "entrada")
        .scalar() or 0
    )

    total_saidas = (
        FluxoCaixa.query.with_entities(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "saida")
        .scalar() or 0
    )

    saldo_total = total_entradas - total_saidas

    # Quantidade total de serviços cadastrados
    total_servicos = Servico.query.count()

    # Quantidade total de agendamentos
    total_agendamentos = Agendamento.query.count()

    return templates.TemplateResponse(
        "relatorios.html",
        {
            "request": request,
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo_total": saldo_total,
            "total_servicos": total_servicos,
            "total_agendamentos": total_agendamentos,
        },
    )
