from django.contrib import admin

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.disponibilidade import Disponibilidade
from core.models.professor import Professor


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "carga_horaria_maxima_semanal")
    search_fields = ("nome",)
    list_filter = ("areas",)


@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ("professor", "dia_semana", "horario_inicio", "horario_fim")
    list_filter = ("dia_semana",)


admin.site.register(Disciplina)
admin.site.register(Alocacao)
