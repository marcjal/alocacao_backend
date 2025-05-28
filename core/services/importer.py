import json
import logging

import pandas as pd
from django.db import transaction

from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.serializers.professor import ProfessorSerializer
from core.models import Importacao

logger = logging.getLogger(__name__)


def processar_importacao(import_id):
    imp = Importacao.objects.get(id=import_id)
    imp.status = "processing"
    imp.erros = []
    imp.save()

    try:
        # 1) Ler o arquivo CSV ou XLSX
        path = imp.file.path
        if path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path)
        else:
            # Aqui adicionamos escapechar para lidar com \" no CSV
            df = pd.read_csv(
                path, encoding="utf-8-sig", escapechar="\\", quotechar='"'
            )

        # 2) Transformar num registro por linha
        registros = df.to_dict(orient="records")
        serializers = []
        erros = []

        # 3) Validação em lote
        for idx, data in enumerate(registros):
            if imp.tipo == "professores" and isinstance(
                data.get("areas"), str
            ):
                try:
                    # Tenta converter JSON-string em lista
                    data["areas"] = json.loads(data["areas"])
                except json.JSONDecodeError:
                    # Fallback caso venha algo como Física;Química
                    data["areas"] = [
                        s.strip()
                        for s in data["areas"].split(";")
                        if s.strip()
                    ]

            serializer = (
                ProfessorSerializer(data=data)
                if imp.tipo == "professores"
                else DisciplinaSerializer(data=data)
            )

            if not serializer.is_valid():
                erros.append({"linha": idx + 1, "errors": serializer.errors})
            else:
                serializers.append(serializer)

        imp.registros_total = len(registros)
        imp.registros_erro = len(erros)
        imp.erros = erros

        # Abort se tiver qualquer erro de validação
        if erros:
            imp.status = "error"
            imp.save()
            return

        # 4) Salvamento atômico
        sucesso = 0
        with transaction.atomic():
            for s in serializers:
                s.save()
                sucesso += 1

        imp.registros_sucesso = sucesso
        imp.status = "done"
        imp.erros = []
        imp.save()

    except Exception as e:
        logger.exception(f"Falha ao processar importacao {import_id}")
        imp.status = "error"
        imp.erros = [{"linha": None, "errors": str(e)}]
        imp.save()
