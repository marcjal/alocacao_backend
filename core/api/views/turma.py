from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.api.serializers.turma import TurmaSerializer
from core.models.turma import Turma


class TurmaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Turma
    """

    queryset = Turma.objects.all().order_by("nome")
    serializer_class = TurmaSerializer
    permission_classes = [AllowAny]
