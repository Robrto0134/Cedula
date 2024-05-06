from rest_framework import serializers
from .models import Mesario

class MesarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesario
        fields = ('nome', 'documento', 'chave_de_acesso')


class CreateMesarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesario
        fields = ('nome', 'documento', 'chave_de_acesso')