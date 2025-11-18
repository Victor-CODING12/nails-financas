from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import date

from ..models.base import get_db
from ..models.fluxo_caixa import FluxoCaixa

router = APIRouter(prefix="/api/fluxo-caixa", tags=["Fluxo de Caixa"])


# ================================
# LISTAR LANÇAMENTOS
# ================================
@router.get("")
def listar_lancamentos(request: Request, db: Session = Depends(get_db)):
    empresa_id = request.state.empresa_id

    lancamentos = (
        db.query(FluxoCaixa)
        .filter(FluxoCaixa.empresa_id == empresa_id)
        .order_by(FluxoCaixa.data.desc())
        .all()
    )

    return [l.to_dict() for l in lancamentos]


# ================================
# CRIAR LANÇAMENTO
# ================================
@router.post("")
def criar_lancamento(
    request: Request,
    tipo: str,
    valor: float,
    data_lancamento: date | None = None,
    descricao: str | None = None,
    categoria: str | None = None,
    db: Session = Depends(get_db),
):
    empresa_id = request.state.empresa_id

    lanc = FluxoCaixa(
        tipo=tipo,
        valor=valor,
        data=data_lancamento or date.today(),
        descricao=descricao,
        categoria=categoria,
        empresa_id=empresa_id,
    )

    db.add(lanc)
    db.commit()
    db.refresh(lanc)

    return lanc.to_dict()
