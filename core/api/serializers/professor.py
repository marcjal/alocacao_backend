from rest_framework import serializers

from core.models.professor import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = [
            "id",
            "nome",
            "areas",
            "carga_horaria_maxima_semanal",
        ]

        read_only_fields = ["id"]
