from django.contrib import admin

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "carga_horaria_maxima_semanal")
    search_fields = ("nome",)
    list_filter = ("areas",)


admin.site.register(Disciplina)
admin.site.register(Alocacao)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "disciplina",
        "dia_semana",
        "horario_inicio",
        "horario_fim",
    )
    list_filter = ("disciplina__area", "dia_semana")
    search_fields = ("nome", "disciplina__nome")
