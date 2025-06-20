import uuid

from django.db import models

from core.models.disciplina import Disciplina

from .base import TimeStampedModel
from .dia_semana import DiaSemana


class Turma(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(
        max_length=100, help_text="Ex: '1A', 'Turma B', 'Manhã', etc."
    )
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="turmas"
    )
    local = models.CharField(
        max_length=100,
        help_text="Local (ex.: 'Porto Alegre', 'São Leopoldo')",
        null=True,
        blank=True,
    )
    dia_semana = models.CharField(
        max_length=10,
        choices=DiaSemana.choices,
        help_text="Dia da semana em que essa turma tem aula semanal",
        null=True,
        blank=True,
    )
    horario_inicio = models.TimeField(
        help_text="Horário de início da aula (HH:MM:SS)", null=True, blank=True
    )
    horario_fim = models.TimeField(
        help_text="Horário de término da aula (HH:MM:SS)",
        null=True,
        blank=True,
    )
    modelo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Modelo (presencial, remoto, híbrido etc.)",
    )
    numero_alunos = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Número de alunos matriculados (para relatórios)",
    )
    tipo_turma = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Tipo de turma (teoria, prática, TCC etc.)",
    )
    periodo = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Período (ex.: '2025.1')",
    )
    orientacoes = models.TextField(
        null=True, blank=True, help_text="Orientações para Secretarias"
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["disciplina", "nome"]

    def __str__(self):
        return f"{self.disciplina.nome} – {self.nome}"
