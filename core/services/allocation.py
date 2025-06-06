from django.db import transaction
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from core.models.alocacao import Alocacao
from core.models.professor import Professor
from core.models.turma import Turma


def run_allocation(recalculate_all=False):
    """
    Executa a alocação automática de professores em Turmas.
    Cada Turma define:
      - dia_semana       (texto, ex.: "segunda", "terca", etc.)
      - horario_inicio   (TimeField)
      - horario_fim      (TimeField)

    Se recalculate_all for False, aloca apenas Turmas que ainda não tenham Alocacao.
    Retorna lista de instâncias de Alocacao criadas.
    """

    if recalculate_all:
        Alocacao.objects.all().delete()

    turmas = Turma.objects.filter(alocacoes__isnull=True)

    professores = list(
        Professor.objects.all().annotate(
            carga_atual=Coalesce(Sum("alocacoes__horas_alocadas"), Value(0))
        )
    )
    for p in professores:
        p.carga_atual = p.carga_atual or 0

    alocacoes_criadas = []

    with transaction.atomic():
        for turma in turmas:
            from datetime import date, datetime

            hi = datetime.combine(date.min, turma.horario_inicio)
            hf = datetime.combine(date.min, turma.horario_fim)
            diff_horas = (hf - hi).total_seconds() / 3600
            if diff_horas <= 0:
                carga_turma = 1
            else:
                carga_turma = int(diff_horas)

            candidatos = [
                prof
                for prof in professores
                if turma.disciplina.area in prof.areas
            ]
            candidatos.sort(key=lambda prof: prof.carga_atual)

            escolhido = None

            for prof in candidatos:
                if (
                    prof.carga_atual + carga_turma
                    > prof.carga_horaria_maxima_semanal
                ):
                    continue

                conflito = Alocacao.objects.filter(
                    professor=prof,
                    turma__dia_semana=turma.dia_semana,
                    turma__horario_inicio__lt=turma.horario_fim,
                    turma__horario_fim__gt=turma.horario_inicio,
                ).exists()

                if conflito:
                    continue

                escolhido = prof
                break

            if escolhido:
                al = Alocacao.objects.create(
                    turma=turma,
                    professor=escolhido,
                    horas_alocadas=carga_turma,
                    status_conflito=False,
                )
                escolhido.carga_atual += carga_turma
            else:
                if candidatos:
                    prof = candidatos[0]
                    al = Alocacao.objects.create(
                        turma=turma,
                        professor=prof,
                        horas_alocadas=carga_turma,
                        status_conflito=True,
                    )
                    prof.carga_atual += carga_turma
                else:
                    al = Alocacao.objects.create(
                        turma=turma,
                        professor=None,
                        horas_alocadas=carga_turma,
                        status_conflito=True,
                    )

            alocacoes_criadas.append(al)

    return alocacoes_criadas
