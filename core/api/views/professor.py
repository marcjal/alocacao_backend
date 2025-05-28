from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from core.api.serializers.professor import ProfessorSerializer
from core.models.professor import Professor


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [AllowAny]
