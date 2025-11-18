from fastapi.templating import Jinja2Templates
import os

from ..utils import format_currency
from ..config import BASE_DIR
from .safe_router import SafeAPIRouter, handle_exceptions

# Shared router and templates object used by the route modules
router = SafeAPIRouter()

# ✔️ Caminho correto onde estão seus templates reais
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'web', 'templates'))

# filtros (mantém igual)
templates.env.filters['format_currency'] = format_currency

# Import routes para registrar
from . import (
    base,
    pagamentos,
    mapeamentos,
    relatorios,
    alertas,
    servicos_routes,
    servicos_api,
    agendamento_routes,
    agendamento_api,
    fluxo_routes,
    fluxo_api,
)

__all__ = ['router', 'templates', 'handle_exceptions']
