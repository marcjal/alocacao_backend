import datetime

from django.db import transaction
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from core.models import Alocacao, Disciplina, Professor


def run_allocation(recalculate_all=False):
    """
    Executa a alocação automática de professores em disciplinas.
    Se recalculate_all for False, aloca apenas disciplinas sem alocação.
    Retorna lista de instâncias de Alocacao criadas.
    """
    # 1) Buscar disciplinas
    if recalculate_all:
        disciplinas = Disciplina.objects.all()
        # limpar alocações antigas, se desejar:
        Alocacao.objects.all().delete()
    else:
        disciplinas = Disciplina.objects.filter(alocacoes__isnull=True)

    # 2) Carregar professores e suas cargas atuais
    professores = list(
        Professor.objects.all().annotate(
            carga_atual=Coalesce(Sum("alocacoes__horas_alocadas"), Value(0))
        )
    )
    # Inicializar carga_atual em zero quando None
    for p in professores:
        p.carga_atual = p.carga_atual or 0

    alocacoes_criadas = []

    # 3) Processar cada disciplina
    with transaction.atomic():
        for disc in disciplinas:
            # calcular duração em horas
            duração = (
                datetime.datetime.combine(datetime.date.today(), disc.horario_fim)
                - datetime.datetime.combine(datetime.date.today(), disc.horario_inicio)
            ).seconds / 3600

            # filtrar candidatos
            candidatos = []
            for prof in professores:
                # área compatível?
                if disc.area not in prof.areas:
                    continue
                # sem conflito de horário?
                conflict = prof.indisponibilidades.filter(
                    dia_semana=disc.dia_semana,
                    horario_inicio__lt=disc.horario_fim,
                    horario_fim__gt=disc.horario_inicio,
                ).exists()
                if conflict:
                    continue
                # carga restante suficiente?
                if prof.carga_atual + duração > prof.carga_horaria_maxima_semanal:
                    continue
                candidatos.append(prof)

            # ordenar por menor carga atual (balanceamento)
            candidatos.sort(key=lambda p: p.carga_atual)

            # criar Alocacao
            if candidatos:
                selecionado = candidatos[0]
                al = Alocacao.objects.create(
                    disciplina=disc,
                    professor=selecionado,
                    horas_alocadas=duração,
                    status_conflito=False,
                )
                # atualizar carga em memória
                selecionado.carga_atual += duração
            else:
                al = Alocacao.objects.create(
                    disciplina=disc,
                    professor=None,
                    horas_alocadas=duração,
                    status_conflito=True,
                )
            alocacoes_criadas.append(al)

    return alocacoes_criadas
