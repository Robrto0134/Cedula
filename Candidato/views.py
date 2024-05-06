from django.shortcuts import render
from rest_framework import generics, status
from .serializers import CandidatoSerializer, CreateCandidatoSerializer
from .models import Candidato
from Eleicao.models import Eleicao
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

class CandidatoView(APIView):
    serializer_class = CreateCandidatoSerializer
    lookup_url_kwarg = 'numero'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            candidato = Candidato.objects.filter(numero=code)
            if len(candidato) > 0:
                data = CandidatoSerializer(candidato[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Candidato nao encontrado': 'Numero Invalido.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Numero nao fornecido'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        cod_eleicao = request.data['cod_eleicao']
        if serializer.is_valid():

            nome = serializer.data.get('nome')
            numero = serializer.data.get('numero')
            foto = serializer.data.get('foto')

            if not Eleicao.objects.filter(codigo=cod_eleicao).exists():
                return Response({'Bad Request': 'Eleicao nao existe...'}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get('votos'):
                votos = serializer.data.get('votos')
            else:
                votos = 0
            eleicao = Eleicao.objects.filter(codigo=cod_eleicao).first()
            queryset = Candidato.objects.filter(numero=numero)
            if queryset.exists():
                candidato = queryset[0]
                candidato.nome = nome
                candidato.numero = numero
                candidato.eleicao = eleicao
                candidato.votos = votos
                candidato.save(update_fields=['nome', 'numero', 'eleicao', 'votos'])
                data = CandidatoSerializer(candidato).data
                data.pop('eleicao')
                data["cod_eleicao"] = cod_eleicao
                return Response(data, status=status.HTTP_200_OK)
            else:
                candidato = Candidato(nome=nome, numero=numero, eleicao=eleicao, votos=0, foto=foto)
                candidato.save()
                return Response(CandidatoSerializer(candidato).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

