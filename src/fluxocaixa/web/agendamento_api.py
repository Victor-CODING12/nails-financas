# src/fluxocaixa/web/agendamento_api.py

from fastapi import APIRouter, HTTPException, Request, Depends
from datetime import date, time, datetime
from sqlalchemy.orm import Session

from ..models.base import get_db
from ..models import Agendamento, Usuario, Empresa
from ..models.fluxo_caixa import FluxoCaixa
from ..auth.auth import usuario_atual

router = APIRouter(prefix="/api/agendamentos", tags=["Agendamentos"])


# ===============================================================
# 🔹 LISTAR AGENDAMENTOS POR EMPRESA
# ===============================================================
@router.get("")
def listar_agendamentos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual),
):
    agendamentos = (
        db.query(Agendamento)
        .filter(Agendamento.empresa_id == usuario.empresa_id)
        .order_by(Agendamento.data, Agendamento.hora)
        .all()
    )

    return [
        {
            "id": a.id,
            "cliente": a.cliente,
            "data": a.data.strftime("%Y-%m-%d") if a.data else "",
            "hora": a.hora.strftime("%H:%M") if a.hora else "",
            "procedimento": a.procedimento,
            "pagamento": a.pagamento or "",
            "valor_servico": float(a.valor_servico or 0),
            "valor_sinal": float(a.valor_sinal or 0),
            "falta_pagar": max(float((a.valor_servico or 0) - (a.valor_sinal or 0)), 0),
            "observacoes": a.observacoes or "",
            "status": a.status or "Pendente",
        }
        for a in agendamentos
    ]


# ===============================================================
# 🔥 Função auxiliar — validação de agenda
# ===============================================================
def validar_agenda_empresa(empresa: Empresa, data_formatada: date, hora_formatada: time):
    # 1 — Validar dia da semana
    dias_map = {
        0: "seg",
        1: "ter",
        2: "qua",
        3: "qui",
        4: "sex",
        5: "sáb",
        6: "dom",
    }

    dia_semana = dias_map[data_formatada.weekday()]

    dias_permitidos = (empresa.dias_funcionamento or "").split(",")

    if dia_semana not in dias_permitidos:
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível agendar para {dia_semana.upper()}. "
                   f"A empresa só atende nos dias: {', '.join(dias_permitidos).upper()}."
        )

    # 2 — Validar horário de funcionamento
    if hora_formatada < empresa.horario_abre or hora_formatada > empresa.horario_fecha:
        raise HTTPException(
            status_code=400,
            detail=f"Horário inválido! O atendimento é apenas entre "
                   f"{empresa.horario_abre.strftime('%H:%M')} e {empresa.horario_fecha.strftime('%H:%M')}."
        )


# ===============================================================
# 🔹 CRIAR AGENDAMENTO
# ===============================================================
@router.post("")
async def criar_agendamento(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual),
):
    dados = await request.json()

    try:
        data_formatada = date.fromisoformat(dados.get("data"))
        hora_formatada = time.fromisoformat(dados.get("hora"))

        empresa = db.query(Empresa).filter_by(id=usuario.empresa_id).first()

        # 🔥 Validar regras de agenda
        validar_agenda_empresa(empresa, data_formatada, hora_formatada)

        valor_servico = float(str(dados.get("valor_servico") or "0").replace(",", "."))
        valor_sinal = float(str(dados.get("valor_sinal") or "0").replace(",", "."))
        status = (dados.get("status") or "Pendente").strip().lower()

        novo = Agendamento(
            cliente=dados.get("cliente"),
            data=data_formatada,
            hora=hora_formatada,
            procedimento=dados.get("procedimento"),
            pagamento=dados.get("pagamento"),
            valor_servico=valor_servico,
            valor_sinal=valor_sinal,
            observacoes=dados.get("observacoes", ""),
            status=status.capitalize(),
            empresa_id=usuario.empresa_id,
        )

        db.add(novo)
        db.commit()
        db.refresh(novo)

        # 🔥 Fluxo automático
        palavras_entrada = ["pago", "concluido", "concluído", "finalizado", "sinal"]

        if any(p in status for p in palavras_entrada):
            valor = valor_sinal if "sinal" in status else valor_servico
            descricao = f"{novo.procedimento} - {novo.cliente}"

            existente = (
                db.query(FluxoCaixa)
                .filter_by(descricao=descricao, empresa_id=usuario.empresa_id)
                .first()
            )

            if not existente and valor > 0:
                db.add(
                    FluxoCaixa(
                        tipo="entrada",
                        descricao=descricao,
                        valor=valor,
                        data=datetime.now().date(),
                        categoria="Serviço",
                        empresa_id=usuario.empresa_id,
                    )
                )
                db.commit()

        return {"success": True, "message": "Agendamento criado com sucesso!"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ===============================================================
# 🔹 EDITAR AGENDAMENTO
# ===============================================================
@router.put("/{id}")
async def atualizar_agendamento(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual),
):
    agendamento = db.get(Agendamento, id)

    if not agendamento or agendamento.empresa_id != usuario.empresa_id:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    dados = await request.json()

    try:
        # Se data/hora forem alteradas → validar
        if "data" in dados or "hora" in dados:
            empresa = db.query(Empresa).filter_by(id=usuario.empresa_id).first()

            nova_data = date.fromisoformat(dados.get("data")) if dados.get("data") else agendamento.data
            nova_hora = time.fromisoformat(dados.get("hora")) if dados.get("hora") else agendamento.hora

            validar_agenda_empresa(empresa, nova_data, nova_hora)

            agendamento.data = nova_data
            agendamento.hora = nova_hora

        # Atualizações comuns
        agendamento.cliente = dados.get("cliente", agendamento.cliente)
        agendamento.procedimento = dados.get("procedimento", agendamento.procedimento)
        agendamento.pagamento = dados.get("pagamento", agendamento.pagamento)
        agendamento.observacoes = dados.get("observacoes", agendamento.observacoes)

        novo_status = (dados.get("status", agendamento.status)).lower()
        agendamento.status = novo_status.capitalize()

        valor_servico = float(str(dados.get("valor_servico") or agendamento.valor_servico or 0))
        valor_sinal = float(str(dados.get("valor_sinal") or agendamento.valor_sinal or 0))
        agendamento.valor_servico = valor_servico
        agendamento.valor_sinal = valor_sinal

        descricao = f"{agendamento.procedimento} - {agendamento.cliente}"
        palavras_entrada = ["pago", "concluido", "concluído", "finalizado", "sinal"]

        # 🔥 Fluxo de caixa (update)
        entrada = (
            db.query(FluxoCaixa)
            .filter_by(descricao=descricao, empresa_id=usuario.empresa_id)
            .first()
        )

        if any(p in novo_status for p in palavras_entrada):
            valor = valor_sinal if "sinal" in novo_status else valor_servico

            if entrada:
                entrada.valor = valor
                entrada.data = datetime.now().date()
            else:
                db.add(
                    FluxoCaixa(
                        tipo="entrada",
                        descricao=descricao,
                        valor=valor,
                        data=datetime.now().date(),
                        categoria="Serviço",
                        empresa_id=usuario.empresa_id,
                    )
                )
        else:
            if entrada:
                db.delete(entrada)

        db.commit()
        return {"success": True, "message": "Agendamento atualizado com sucesso!"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ===============================================================
# 🔹 EXCLUIR AGENDAMENTO
# ===============================================================
@router.delete("/{id}")
def excluir_agendamento(
    id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_atual),
):
    agendamento = db.get(Agendamento, id)

    if not agendamento or agendamento.empresa_id != usuario.empresa_id:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")

    db.delete(agendamento)
    db.commit()

    return {"success": True, "message": "Agendamento excluído com sucesso!"}
