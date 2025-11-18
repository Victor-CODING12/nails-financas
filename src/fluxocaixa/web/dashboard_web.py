# src/fluxocaixa/web/dashboard_web.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/dashboard", name="dashboard")
@handle_exceptions
async def pagina_dashboard(request: Request):
    """
    Página principal do Dashboard Web.
    Protegida pelo middleware e acessível somente para usuários logados.
    """

    contexto = {
        "request": request,
        "empresa_id": request.state.empresa_id,
        "usuario_email": request.state.user_email,
    }

    return templates.TemplateResponse("dashboard.html", contexto)
