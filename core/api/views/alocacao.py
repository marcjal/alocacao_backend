import csv
import io

import pandas as pd
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.serializers.alocacao import AlocacaoSerializer
from core.models import Alocacao
from core.services.allocation import run_allocation


class AlocacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AlocacaoSerializer
    queryset = Alocacao.objects.all()

    @action(detail=False, methods=["post"])
    def auto(self, request):
        alocs = run_allocation()
        serializer = self.get_serializer(alocs, many=True)
        return Response(serializer.data)

    # @action(detail=False, methods=['get'], url_path='export')
    # def export(self, request, **kwargs):
    #     # primeiro, tenta pegar o format vindo da rota estática via kwargs
    #     fmt = kwargs.get('format') or request.query_params.get('format', 'csv')
    #     fmt = fmt.lower()

    #     qs = Alocacao.objects.select_related('disciplina', 'professor').all()

    #     rows = []
    #     for al in qs:
    #         rows.append({
    #             'Código atividade': str(al.disciplina.id),
    #             'Nome da Atividade': al.disciplina.nome,
    #             'Dia da Semana': al.disciplina.dia_semana,
    #             'Horário início': al.disciplina.horario_inicio.strftime('%H:%M:%S'),
    #             'Horário fim': al.disciplina.horario_fim.strftime('%H:%M:%S'),
    #             'Professor': al.professor.nome if al.professor else '',
    #             'Horas alocadas': al.horas_alocadas,
    #             'Status conflito': '⚠️' if al.status_conflito else 'OK'
    #         })

    #     if fmt == 'xlsx':
    #         buffer = io.BytesIO()
    #         pd.DataFrame(rows).to_excel(buffer, index=False)
    #         buffer.seek(0)
    #         content = buffer.getvalue()
    #         content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #         filename = 'alocacoes.xlsx'
    #     else:
    #         buffer = io.StringIO()
    #         writer = csv.DictWriter(buffer, fieldnames=rows[0].keys() if rows else [])
    #         writer.writeheader()
    #         writer.writerows(rows)
    #         content = buffer.getvalue()
    #         content_type = 'text/csv'
    #         filename = 'alocacoes.csv'

    #     resp = HttpResponse(content, content_type=content_type)
    #     resp['Content-Disposition'] = f'attachment; filename="{filename}"'
    #     return resp
