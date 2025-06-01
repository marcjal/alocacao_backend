from rest_framework import status, viewsets
from rest_framework.response import Response

from core.api.serializers.importacao import ImportacaoSerializer
from core.models.importacao import Importacao
from core.services.importer import processar_importacao


class ImportacaoViewSet(viewsets.ModelViewSet):
    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        importacao = serializer.save()
        processar_importacao(importacao.id)
        return Response(
            self.get_serializer(importacao).data,
            status=status.HTTP_201_CREATED,
        )
