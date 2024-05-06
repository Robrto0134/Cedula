from rest_framework import serializers
from .models import Candidato

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = ('nome', 'foto', 'numero', 'eleicao', 'votos')


class CreateCandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = ('nome', 'foto', 'numero', 'eleicao', 'votos')