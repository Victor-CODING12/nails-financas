from fastapi import Request
from .safe_router import SafeAPIRouter, handle_exceptions
from . import templates

router = SafeAPIRouter()


@router.get("/fluxo-caixa", name="fluxo_caixa")
@handle_exceptions
async def fluxo_caixa(request: Request):
    """
    Página do Fluxo de Caixa — protegida automaticamente pelo middleware.
    """

    contexto = {
        "request": request,
        "empresa_id": request.state.empresa_id,
        "usuario_email": request.state.user_email,
        "usuario_id": request.state.user_id
    }

    return templates.TemplateResponse("fluxo_caixa.html", contexto)
