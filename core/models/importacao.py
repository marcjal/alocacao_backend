import uuid
from django.db import models
from .base import TimeStampedModel

class Importacao(TimeStampedModel):
    TIPOS = [
        ('disciplinas', 'Disciplinas'),
        ('professores', 'Professores'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    file = models.FileField(upload_to='imports/')
    status = models.CharField(
        max_length=10,
        choices=[('pending','Pendente'),('processing','Processando'),('done','Concluído'),('error','Erro')],
        default='pending'
    )
    registros_total = models.IntegerField(default=0)
    registros_sucesso = models.IntegerField(default=0)
    registros_erro = models.IntegerField(default=0)
