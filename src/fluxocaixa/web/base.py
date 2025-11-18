from fastapi import Request, Depends
from ..auth.current_user_web import usuario_atual_web
from . import router, templates
from ..models import FluxoCaixa, Agendamento, Servico
from sqlalchemy import func


# ============================
# DASHBOARD PRINCIPAL
# ============================

@router.get("/")
async def index(request: Request, usuario=Depends(usuario_atual_web)):
    # TOTAL DE ENTRADAS
    total_entradas = (
        FluxoCaixa.query.with_entities(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "entrada")
        .scalar() or 0
    )

    # TOTAL DE SAÍDAS
    total_saidas = (
        FluxoCaixa.query.with_entities(func.sum(FluxoCaixa.valor))
        .filter(FluxoCaixa.tipo == "saida")
        .scalar() or 0
    )

    # SALDO
    saldo = total_entradas - total_saidas

    # QUANTIDADE DE AGENDAMENTOS DO DIA
    agendamentos_hoje = (
        Agendamento.query.filter(
            func.date(Agendamento.data) == func.current_date()
        ).count()
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "saldo": saldo,
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "agendamentos_hoje": agendamentos_hoje,
        },
    )


# ============================
# PÁGINA DE RELATÓRIOS
# ============================

@router.get("/relatorios")
async def relatorios(request: Request, usuario=Depends(usuario_atual_web)):
    return templates.TemplateResponse("relatorios.html", {"request": request})


# ============================
# PÁGINA DE SERVIÇOS
# ============================

@router.get("/servicos")
async def servicos(request: Request, usuario=Depends(usuario_atual_web)):
    lista = Servico.query.all()
    return templates.TemplateResponse(
        "servicos.html", {"request": request, "servicos": lista}
    )


# ============================
# PÁGINA DE AGENDAMENTOS
# ============================

@router.get("/agendamento")
async def pagina_agendamento(request: Request, usuario=Depends(usuario_atual_web)):
    return templates.TemplateResponse("agendamento.html", {"request": request})

