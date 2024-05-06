from rest_framework import serializers
from .models import Eleitor

class EleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = ('nome', 'foto', 'documento', 'pode_votar')


class CreateEleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = ('nome', 'documento', 'foto')