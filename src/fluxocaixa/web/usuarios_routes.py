# src/fluxocaixa/web/usuarios_routes.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/usuarios", name="usuarios")
@handle_exceptions
async def pagina_usuarios(request: Request):
    """
    Página de gerenciamento de usuários (WEB)
    Acessível apenas se estiver logado.
    """
    contexto = {
        "request": request,
        "empresa_id": request.state.empresa_id,
        "usuario_email": request.state.user_email,
    }

    return templates.TemplateResponse("usuarios.html", contexto)
