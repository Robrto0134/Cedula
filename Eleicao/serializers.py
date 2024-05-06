from rest_framework import serializers
from .models import Eleicao

class EleicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleicao
        fields = ('codigo',)


class CreateEleicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleicao
        fields = ('codigo',)