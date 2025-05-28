from rest_framework import serializers

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


class AlocacaoGenSerializer(serializers.Serializer):
    coordenacao = serializers.CharField(required=False, allow_blank=True)
    codigo_atividade = serializers.CharField()
    nome_atividade = serializers.CharField()
    codigo_turma = serializers.CharField(required=False, allow_blank=True)
    id_turma = serializers.UUIDField(required=False)
    local = serializers.CharField(required=False, allow_blank=True)
    modelo = serializers.CharField(required=False, allow_blank=True)
    num_alunos = serializers.IntegerField(required=False)
    tipo_turma = serializers.CharField(required=False, allow_blank=True)
    periodo = serializers.CharField(required=False, allow_blank=True)
    creditos = serializers.CharField(required=False, allow_blank=True)
    dia_semana = serializers.CharField()
    horario_inicio = serializers.TimeField()
    horario_fim = serializers.TimeField()
    tipo_atividade = serializers.CharField(required=False, allow_blank=True)
    carga_docente = serializers.IntegerField()
    chapa = serializers.CharField()
    professor_nome = serializers.CharField()
    horas_a_alocar = serializers.IntegerField()
    orientacoes = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        prof_defaults = {
            "nome": validated_data["professor_nome"],
            "areas": [],
            "carga_horaria_maxima_semanal": validated_data["carga_docente"],
        }
        prof, _ = Professor.objects.update_or_create(
            chapa=validated_data["chapa"], defaults=prof_defaults
        )

        disc_defaults = {
            "area": validated_data.get("tipo_atividade", ""),
            "creditos_academicos": validated_data.get("creditos", ""),
        }
        disc, _ = Disciplina.objects.update_or_create(
            nome=validated_data["nome_atividade"], defaults=disc_defaults
        )

        turma_defaults = {
            "disciplina": disc,
            "nome": validated_data.get("codigo_turma")
            or str(validated_data.get("id_turma")),
            "local": validated_data.get("local", ""),
            "modelo": validated_data.get("modelo", ""),
            "numero_alunos": validated_data.get("num_alunos"),
            "tipo_turma": validated_data.get("tipo_turma", ""),
            "periodo": validated_data.get("periodo", ""),
            "dia_semana": validated_data["dia_semana"],
            "horario_inicio": validated_data["horario_inicio"],
            "horario_fim": validated_data["horario_fim"],
            "orientacoes": validated_data.get("orientacoes", ""),
        }
        turma, _ = Turma.objects.update_or_create(
            id=validated_data.get("id_turma"), defaults=turma_defaults
        )

        aloc = Alocacao.objects.create(
            turma=turma,
            professor=prof,
            horas_alocadas=validated_data["horas_a_alocar"],
            status_conflito=False,
        )
        return aloc
