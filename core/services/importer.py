import json
import logging

import pandas as pd
from django.db import IntegrityError, transaction

from core.api.serializers.alocacao_gen import AlocacaoGenSerializer
from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.serializers.professor import ProfessorSerializer
from core.models.importacao import Importacao

logger = logging.getLogger(__name__)


def processar_importacao(import_id):
    imp = Importacao.objects.get(id=import_id)
    imp.status = "processing"
    imp.save(update_fields=["status"])

    try:
        path = imp.file.path
        if path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path, dtype=str).fillna("")
        else:
            df = pd.read_csv(
                path,
                encoding="utf-8-sig",
                escapechar="\\",
                quotechar='"',
                dtype=str,
                na_filter=False,
                keep_default_na=False,
            )

        headers = set(df.columns)
        if {"nome", "areas", "carga_horaria_maxima_semanal"}.issubset(headers):
            tipo = "professores"
        elif {"nome", "area"}.issubset(headers):
            tipo = "disciplinas"
        else:
            tipo = "alocacoes"

        registros = df.to_dict(orient="records")
        serializers = []
        erros = []

        for idx, data in enumerate(registros, start=1):
            if tipo == "professores" and isinstance(data.get("areas"), str):
                try:
                    data["areas"] = json.loads(data["areas"])
                except json.JSONDecodeError:
                    data["areas"] = [
                        s.strip()
                        for s in data["areas"].split(";")
                        if s.strip()
                    ]

            if tipo == "professores":
                ser = ProfessorSerializer(data=data)
            elif tipo == "disciplinas":
                ser = DisciplinaSerializer(data=data)
            else:
                ser = AlocacaoGenSerializer(data=data)

            if not ser.is_valid():
                erros.append((idx, ser.errors))
            else:
                serializers.append((idx, ser))

        imp.registros_total = len(registros)
        imp.registros_erro = len(erros)
        imp.save(update_fields=["registros_total", "registros_erro"])

        if erros:
            imp.status = "error"
            imp.save(update_fields=["status"])
            return

        sucesso = 0
        for idx, ser in serializers:
            try:
                with transaction.atomic():
                    ser.save()
                sucesso += 1
            except IntegrityError:
                logger.warning(f"Linha {idx}: registro duplicado, skip.")
                sucesso += 1
            except Exception as exc:
                logger.error(
                    f"Linha {idx}: falha inesperada – {exc}", exc_info=True
                )
                erros.append((idx, str(exc)))

        imp.registros_sucesso = sucesso
        imp.registros_erro = len(erros)
        imp.status = "done" if not erros else "error"
        imp.save(
            update_fields=["registros_sucesso", "registros_erro", "status"]
        )

    except Exception as e:
        logger.exception(f"Falha ao processar importacao {import_id}")
        imp.status = "error"
        imp.registros_erro = imp.registros_total or 0
        imp.save(update_fields=["status", "registros_erro"])
