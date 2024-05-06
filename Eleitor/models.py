from django.db import models

class Eleitor(models.Model):
    nome = models.CharField(default="Lula", max_length=666, null=False)
    foto = models.ImageField(null=True)
    documento = models.CharField(max_length=666, null=False)
    pode_votar = models.SmallIntegerField(default=0)


