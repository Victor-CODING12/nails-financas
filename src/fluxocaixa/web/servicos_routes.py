# src/fluxocaixa/web/servicos_routes.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/servicos", name="servicos")
@handle_exceptions
async def pagina_servicos(request: Request):
    """
    Página de listagem e cadastro de serviços.
    Agora protegida pelo middleware de autenticação.
    """

    contexto = {
        "request": request,
        "empresa_id": getattr(request.state, "empresa_id", None),
        "usuario_email": getattr(request.state, "user_email", None),
    }

    return templates.TemplateResponse("servicos.html", contexto)
