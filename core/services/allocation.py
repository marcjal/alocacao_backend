import datetime

from django.db import transaction
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor


def run_allocation(recalculate_all=False):
    """
    Executa a alocação automática de professores em disciplinas.
    Se recalculate_all for False, aloca apenas disciplinas sem alocação.
    Retorna lista de instâncias de Alocacao criadas.
    """
    if recalculate_all:
        disciplinas = Disciplina.objects.all()
        Alocacao.objects.all().delete()
    else:
        disciplinas = Disciplina.objects.filter(alocacoes__isnull=True)

    professores = list(
        Professor.objects.all().annotate(
            carga_atual=Coalesce(Sum("alocacoes__horas_alocadas"), Value(0))
        )
    )
    for p in professores:
        p.carga_atual = p.carga_atual or 0

    alocacoes_criadas = []

    with transaction.atomic():
        for disc in disciplinas:
            duração = (
                datetime.datetime.combine(
                    datetime.date.today(), disc.horario_fim
                )
                - datetime.datetime.combine(
                    datetime.date.today(), disc.horario_inicio
                )
            ).seconds / 3600

            candidatos = []
            for prof in professores:
                if disc.area not in prof.areas:
                    continue
                conflict = prof.disponibilidade.filter(
                    dia_semana=disc.dia_semana,
                    horario_inicio__lt=disc.horario_fim,
                    horario_fim__gt=disc.horario_inicio,
                ).exists()
                if conflict:
                    continue
                if (
                    prof.carga_atual + duração
                    > prof.carga_horaria_maxima_semanal
                ):
                    continue
                candidatos.append(prof)

            candidatos.sort(key=lambda p: p.carga_atual)

            if candidatos:
                selecionado = candidatos[0]
                al = Alocacao.objects.create(
                    disciplina=disc,
                    professor=selecionado,
                    horas_alocadas=duração,
                    status_conflito=False,
                )
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
