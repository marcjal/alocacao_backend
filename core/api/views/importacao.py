import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status, viewsets
from rest_framework.response import Response

from core.api.serializers.importacao import ImportacaoSerializer
from core.models.importacao import Importacao
from core.services.importer import processar_importacao


class ImportacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para criar jobs de importação de planilhas.
    Suporta:
      1) multipart/form-data (com campo 'file')
      2) JSON com Base64 (campos 'filename' e 'content_base64')
    """

    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        content_b64 = data.get("content_base64")
        filename = data.get("filename")

        if content_b64 and filename:
            if "," in content_b64:
                _, b64_data = content_b64.split(",", 1)
            else:
                b64_data = content_b64

            try:
                file_bytes = base64.b64decode(b64_data)
            except Exception:
                return Response(
                    {"detail": "O campo 'content_base64' está malformado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            uploaded_file = SimpleUploadedFile(
                name=filename,
                content=file_bytes,
                content_type="application/octet-stream",
            )

            data.pop("content_base64")
            data.pop("filename")

            data["file"] = uploaded_file
            request.FILES.clear()
            request.FILES["file"] = uploaded_file

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        imp = serializer.save()

        processar_importacao(imp.id)

        return Response(
            self.get_serializer(imp).data, status=status.HTTP_201_CREATED
        )
