from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.api.serializers.disciplina import DisciplinaSerializer
from core.models.disciplina import Disciplina


class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [AllowAny]
