# src/fluxocaixa/routes/servicos_api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Servico, get_db
from ..auth.current_user_api import usuario_atual_api  # usuário autenticado
from ..models import Usuario

router = APIRouter(prefix="/api/servicos", tags=["Serviços"])


# ===============================================================
# 🔹 LISTAR SERVIÇOS
# ===============================================================
@router.get("")
def listar_servicos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual_api)
):
    servicos = (
        db.query(Servico)
        .filter(Servico.empresa_id == usuario.empresa_id)
        .order_by(Servico.nome.asc())
        .all()
    )

    return [
        {
            "id": s.id,
            "nome": s.nome,
            "valor": s.valor,
            "duracao": s.duracao,
            "descricao": s.descricao or ""
        }
        for s in servicos
    ]


# ===============================================================
# 🔹 CRIAR SERVIÇO
# ===============================================================
@router.post("")
def criar_servico(
    nome: str,
    valor: float,
    duracao: int,
    descricao: str | None = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual_api)
):

    novo = Servico(
        nome=nome,
        valor=valor,
        duracao=duracao,
        descricao=descricao,
        empresa_id=usuario.empresa_id,
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {"success": True, "message": "Serviço criado com sucesso!"}


# ===============================================================
# 🔹 EDITAR SERVIÇO
# ===============================================================
@router.put("/{id}")
def editar_servico(
    id: int,
    nome: str,
    valor: float,
    duracao: int,
    descricao: str | None = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual_api)
):
    servico = db.query(Servico).filter(
        Servico.id == id,
        Servico.empresa_id == usuario.empresa_id
    ).first()

    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    servico.nome = nome
    servico.valor = valor
    servico.duracao = duracao
    servico.descricao = descricao

    db.commit()

    return {"success": True, "message": "Serviço atualizado com sucesso!"}


# ===============================================================
# 🔹 EXCLUIR SERVIÇO
# ===============================================================
@router.delete("/{id}")
def excluir_servico(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual_api)
):

    servico = db.query(Servico).filter(
        Servico.id == id,
        Servico.empresa_id == usuario.empresa_id
    ).first()

    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    db.delete(servico)
    db.commit()

    return {"success": True, "message": "Serviço excluído com sucesso!"}
