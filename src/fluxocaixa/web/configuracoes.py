# src/fluxocaixa/web/configuracoes.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/configuracoes", name="configuracoes")
@handle_exceptions
async def pagina_configuracoes(request: Request):
    """
    Página de Configurações do Sistema.
    Apenas renderiza o template configuracoes.html com os dados do usuário atual.
    """

    contexto = {
        "request": request,
        "empresa_id": request.state.empresa_id,
        "usuario_email": request.state.user_email,
    }

    return templates.TemplateResponse("configuracoes.html", contexto)
