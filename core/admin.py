from django.contrib import admin

from .models import Alocacao, Disciplina, Disponibilidade, Professor


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
