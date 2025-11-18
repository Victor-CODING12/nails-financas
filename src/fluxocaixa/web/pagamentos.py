# src/fluxocaixa/web/pagamentos.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/pagamentos", name="pagamentos")
@handle_exceptions
async def pagina_pagamentos(request: Request):
    """
    Página principal de Pagamentos / Fluxo Financeiro.
    Agora protegida por login e filtrada por empresa_id.
    """

    contexto = {
        "request": request,
        "empresa_id": getattr(request.state, "empresa_id", None),
        "usuario_email": getattr(request.state, "user_email", None),
    }

    return templates.TemplateResponse("pagamentos.html", contexto)
