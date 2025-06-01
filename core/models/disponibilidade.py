import uuid

from django.db import models

from .base import TimeStampedModel
from .dia_semana import DiaSemana
from .professor import Professor


class Disponibilidade(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professor = models.ForeignKey(
        Professor, related_name="disponibilidades", on_delete=models.CASCADE
    )
    dia_semana = models.CharField(max_length=10, choices=DiaSemana.choices)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()

    class Meta:
        verbose_name = "Disponibilidade"
        verbose_name_plural = "Disponibilidades"
        constraints = [
            models.CheckConstraint(
                check=models.Q(horario_inicio__lt=models.F("horario_fim")),
                name="horario_inicio_menor_fim",
            )
        ]

    def __str__(self):
        return f"{
            self.professor.nome} - {
            self.get_dia_semana_display()} {
            self.horario_inicio} às {
                self.horario_fim}"
