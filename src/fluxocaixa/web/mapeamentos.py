# src/fluxocaixa/web/mapeamentos.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/mapeamentos", name="mapeamentos")
@handle_exceptions
async def pagina_mapeamentos(request: Request):
    """
    Página de mapeamentos (categorias, status, pagamentos etc).
    Agora protegida pelo middleware e recebendo dados do usuário logado.
    """

    contexto = {
        "request": request,
        "empresa_id": getattr(request.state, "empresa_id", None),
        "usuario_email": getattr(request.state, "user_email", None),
    }

    return templates.TemplateResponse("mapeamentos.html", contexto)
