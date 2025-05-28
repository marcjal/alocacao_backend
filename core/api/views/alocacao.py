from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.serializers.alocacao import AlocacaoSerializer
from core.models.alocacao import Alocacao
from core.services.allocation import run_allocation


class AlocacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AlocacaoSerializer
    queryset = Alocacao.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["professor"]

    @action(detail=False, methods=["post"])
    def auto(self, request):
        run_allocation()

        qs = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
