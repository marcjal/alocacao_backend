import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .base import TimeStampedModel
from .dia_semana import DiaSemana


class Disciplina(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    dia_semana = models.CharField(
        max_length=10,
        choices=DiaSemana.choices,
        default=DiaSemana.SEGUNDA,
        help_text="Dia da semana de realização da aula",
    )
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    carga_horaria_semanal = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    horas_a_serem_alocadas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["dia_semana", "horario_inicio"]

    def __str__(self):
        return f"{
            self.nome} ({
            self.get_dia_semana_display()} {
            self.horario_inicio}-{
                self.horario_fim})"
