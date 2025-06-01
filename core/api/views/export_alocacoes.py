import base64
import csv
import io

import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.views import View

from core.models.alocacao import Alocacao


class ExportAlocacoesView(View):
    """
    Endpoint estático para exportar alocações em CSV ou XLSX.
    Suporta base64 via query param `as_base64`.
    Formato definido por rota: /export/<format>/
    """

    def get(self, request, *args, **kwargs):
        fmt = kwargs.get("format", "csv").lower()
        as_b64 = request.GET.get("as_base64") in ("1", "true", "yes")

        qs = Alocacao.objects.select_related("disciplina", "professor").all()
        rows = []
        for al in qs:
            rows.append(
                {
                    "Código atividade": str(al.disciplina.id),
                    "Nome da Atividade": al.disciplina.nome,
                    "Dia da Semana": al.disciplina.dia_semana,
                    "Horário início": al.disciplina.horario_inicio.strftime(
                        "%H:%M:%S"
                    ),
                    "Horário fim": al.disciplina.horario_fim.strftime(
                        "%H:%M:%S"
                    ),
                    "Professor": al.professor.nome if al.professor else "",
                    "Horas alocadas": al.horas_alocadas,
                    "Status conflito": "⚠️" if al.status_conflito else "OK",
                }
            )

        if fmt == "xlsx":
            buffer = io.BytesIO()
            pd.DataFrame(rows).to_excel(buffer, index=False)
            buffer.seek(0)
            raw = buffer.getvalue()
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = "alocacoes.xlsx"
        else:
            buffer = io.StringIO()
            writer = csv.DictWriter(
                buffer, fieldnames=rows[0].keys() if rows else []
            )
            writer.writeheader()
            writer.writerows(rows)
            raw = buffer.getvalue().encode("utf-8")
            content_type = "text/csv"
            filename = "alocacoes.csv"

        if as_b64:
            b64 = base64.b64encode(raw).decode("ascii")
            return JsonResponse({"filename": filename, "content": b64})

        resp = HttpResponse(raw, content_type=content_type)
        resp["Content-Disposition"] = f'attachment; filename="{filename}"'
        return resp
