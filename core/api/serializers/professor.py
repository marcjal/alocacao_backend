from rest_framework import serializers

from core.api.serializers.indisponibilidade import IndisponibilidadeSerializer
from core.models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    indisponibilidades = IndisponibilidadeSerializer(many=True, read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "areas",
            "carga_horaria_maxima_semanal",
            "indisponibilidades",
        ]
