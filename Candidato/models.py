from django.db import models

from Eleicao.models import Eleicao

class Candidato(models.Model):
    nome = models.CharField(default="Lula", max_length=666, null=False)
    foto = models.ImageField(null=True)
    votos = models.IntegerField(default=0)
    numero = models.SmallIntegerField(null=False)
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, null=True)




