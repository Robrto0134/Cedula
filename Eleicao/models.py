from django.db import models

from random import randint

def generate_election_id():
    return str(randint(1000, 9999))


class Eleicao(models.Model):
    codigo = models.CharField(default=generate_election_id, max_length=6)
    

