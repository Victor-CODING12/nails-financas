# src/fluxocaixa/web/alertas.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/alertas", name="alertas")
@handle_exceptions
async def pagina_alertas(request: Request):
    """
    Página de alertas e notificações do sistema.
    Acessível somente após login.
    """

    contexto = {
        "request": request,
        "empresa_id": getattr(request.state, "empresa_id", None),
        "usuario_email": getattr(request.state, "user_email", None),
    }

    return templates.TemplateResponse("alertas.html", contexto)
