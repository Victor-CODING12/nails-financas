# src/fluxocaixa/web/agenda_page.py

from fastapi import Request
from . import router, templates, handle_exceptions


@router.get("/agenda", name="agenda")
@handle_exceptions
async def pagina_agenda(request: Request):
    """
    Página da Agenda (Calendário).
    Apenas usuários logados podem acessar.
    """

    contexto = {
        "request": request,
        "empresa_id": getattr(request.state, "empresa_id", None),
        "usuario_email": getattr(request.state, "user_email", None),
    }

    return templates.TemplateResponse("agenda.html", contexto)
