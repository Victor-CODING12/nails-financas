from fastapi import Request
from .safe_router import SafeAPIRouter, handle_exceptions
from . import templates

router = SafeAPIRouter()


@router.get("/agendamento", name="agendamento")
@handle_exceptions
async def pagina_agendamento(request: Request):
    """
    Página de agendamentos — protegida pelo middleware AuthWebMiddleware.

    O middleware já definiu:
        request.state.user_id
        request.state.user_email
        request.state.empresa_id

    Aqui apenas repassamos os dados ao template.
    """

    contexto = {
        "request": request,
        "empresa_id": request.state.empresa_id,
        "usuario_email": request.state.user_email,
        "usuario_id": request.state.user_id
    }

    return templates.TemplateResponse("agendamento.html", contexto)
