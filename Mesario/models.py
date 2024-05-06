from django.db import models
import uuid

class Mesario(models.Model):
    nome = models.CharField(default="Lula", max_length=666, null=False)
    documento = models.CharField(max_length=666, null=False)
    chave_de_acesso = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


