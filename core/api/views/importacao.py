import base64
from io import BytesIO, StringIO

import pandas as pd
from django.core.files.uploadedfile import SimpleUploadedFile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from core.api.serializers.importacao import ImportacaoSerializer
from core.models.importacao import Importacao


class ImportacaoViewSet(viewsets.ModelViewSet):
    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer

    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Importar",
        consumes=["multipart/form-data"],
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Arquivo a importar",
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Importação realizada com sucesso"
            ),
            400: openapi.Response(description="Erro de validação"),
        },
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        content_b64 = data.get("content_base64")
        filename = data.get("filename")
        if content_b64 and filename:
            if "," in content_b64:
                _, content_b64 = content_b64.split(",", 1)
            try:
                raw = base64.b64decode(content_b64)
            except Exception:
                return Response(
                    {"detail": "Campo 'content_base64' malformado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            uploaded_file = SimpleUploadedFile(
                name=filename,
                content=raw,
                content_type="application/octet-stream",
            )
            data.pop("content_base64")
            data.pop("filename")
            data["file"] = uploaded_file
            request.FILES.clear()
            request.FILES["file"] = uploaded_file

        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response(
                {"detail": "Campo 'file' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        name = uploaded.name.lower()
        uploaded.seek(0)
        if name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(BytesIO(uploaded.read()), nrows=0)
        else:
            df = pd.read_csv(
                StringIO(uploaded.read().decode("utf-8-sig")), nrows=0
            )
        cols = {c.lower() for c in df.columns}

        if {"areas", "carga_horaria_maxima_semanal", "chapa"} <= cols:
            tipo = "professores"
        elif (
            "carga_horaria_docente" in cols
            or "tipo atividade acadêmica" in cols
        ):
            tipo = "disciplinas"
        else:
            tipo = "alocacoes"

        data["tipo"] = tipo
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        imp = serializer.save()

        from core.services.importer import processar_importacao

        processar_importacao(imp.id)

        return Response(
            self.get_serializer(imp).data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
