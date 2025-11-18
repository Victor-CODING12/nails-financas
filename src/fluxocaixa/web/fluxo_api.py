from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime, date
from ..models import db, FluxoCaixa
from sqlalchemy import func

router = APIRouter(prefix="/api/fluxo-caixa", tags=["Fluxo de Caixa"])

# ====================================
# 📊 LISTAR LANÇAMENTOS (corrigido para exibir todos)
# ====================================
@router.get("")
async def listar(
    inicio: str | None = Query(None, description="Data inicial no formato YYYY-MM-DD"),
    fim: str | None = Query(None, description="Data final no formato YYYY-MM-DD")
):
    """Lista lançamentos do fluxo de caixa (com ou sem filtros de data)."""
    try:
        query = db.session.query(FluxoCaixa)

        # 🔹 Aplica filtros de data se enviados
        if inicio and fim:
            data_inicio = datetime.strptime(inicio, "%Y-%m-%d").date()
            data_fim = datetime.strptime(fim, "%Y-%m-%d").date()
            query = query.filter(FluxoCaixa.data.between(data_inicio, data_fim))
        elif inicio:
            data_inicio = datetime.strptime(inicio, "%Y-%m-%d").date()
            query = query.filter(FluxoCaixa.data >= data_inicio)
        elif fim:
            data_fim = datetime.strptime(fim, "%Y-%m-%d").date()
            query = query.filter(FluxoCaixa.data <= data_fim)
        # ✅ Se não houver filtro, mostra tudo
        else:
            query = query.order_by(FluxoCaixa.data.desc())

        lancamentos = query.order_by(FluxoCaixa.data.desc()).all()

        total_entradas = sum(l.valor for l in lancamentos if l.tipo == "entrada")
        total_saidas = sum(l.valor for l in lancamentos if l.tipo == "saida")
        saldo_final = total_entradas - total_saidas

        return JSONResponse({
            "lancamentos": [l.to_dict() for l in lancamentos],
            "totais": {
                "total_entradas": round(total_entradas, 2),
                "total_saidas": round(total_saidas, 2),
                "saldo_final": round(saldo_final, 2)
            }
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar lançamentos: {str(e)}")


# ====================================
# ➕ CRIAR NOVO LANÇAMENTO
# ====================================
@router.post("")
async def criar(request: Request):
    """Cria um novo lançamento (entrada ou saída)."""
    try:
        dados = await request.json()
        tipo = dados.get("tipo")
        data_str = dados.get("data")
        valor = float(dados.get("valor", 0))
        descricao = dados.get("descricao", "")
        categoria = dados.get("categoria", "")

        if tipo not in ["entrada", "saida"]:
            raise HTTPException(status_code=400, detail="Tipo inválido. Use 'entrada' ou 'saida'.")

        if not data_str:
            raise HTTPException(status_code=400, detail="Campo 'data' é obrigatório.")

        data = datetime.strptime(data_str, "%Y-%m-%d").date()

        novo = FluxoCaixa(
            tipo=tipo,
            data=data,
            valor=valor,
            descricao=descricao,
            categoria=categoria
        )

        db.session.add(novo)
        db.session.commit()

        return {"status": "ok", "message": "Lançamento criado com sucesso!"}

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar lançamento: {str(e)}")


# ====================================
# ❌ EXCLUIR LANÇAMENTO
# ====================================
@router.delete("/{id}")
async def excluir(id: int):
    """Exclui um lançamento pelo ID."""
    try:
        lancamento = db.session.get(FluxoCaixa, id)
        if not lancamento:
            raise HTTPException(status_code=404, detail="Lançamento não encontrado.")

        db.session.delete(lancamento)
        db.session.commit()

        return {"status": "ok", "message": "Lançamento excluído com sucesso!"}

    except Exception as e:
        db.session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir lançamento: {str(e)}")