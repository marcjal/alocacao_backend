from rest_framework import serializers

from core.api.serializers.disponibilidade import DisponibilidadeSerializer
from core.models.professor import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    disponibilidades = DisponibilidadeSerializer(many=True, read_only=True)

    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "areas",
            "carga_horaria_maxima_semanal",
            "disponibilidades",
        ]
