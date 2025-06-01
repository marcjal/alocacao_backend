from rest_framework import serializers

from core.models.disciplina import Disciplina


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = [
            "id",
            "nome",
            "area",
            "dia_semana",
            "horario_inicio",
            "horario_fim",
            "carga_horaria_semanal",
            "horas_a_serem_alocadas",
        ]
