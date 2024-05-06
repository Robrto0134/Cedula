from django.shortcuts import render
from Candidato.models import Candidato
from Eleitor.models import Eleitor
from rest_framework import generics, status
from .serializers import EleicaoSerializer, CreateEleicaoSerializer
from .models import Eleicao
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

class EleicaoView(APIView):
    serializer_class = CreateEleicaoSerializer
    lookup_url_kwarg = 'codigo'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            eleicao = Eleicao.objects.filter(codigo=code)
            if len(eleicao) > 0:
                data = EleicaoSerializer(eleicao[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Eleicao nao encontrada': 'Codigo invalido .'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Codigo nao informado'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            codigo = serializer.data.get('codigo')
            queryset = Eleicao.objects.filter(codigo=codigo)
            if queryset.exists():
                eleicao = queryset[0]
                eleicao.codigo = codigo
                eleicao.save(update_fields=['codigo'])
                return Response(EleicaoSerializer(eleicao).data, status=status.HTTP_200_OK)
            else:
                eleicao = Eleicao()
                eleicao.save()
                return Response(EleicaoSerializer(eleicao).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class VoteEleicaoView(APIView):
    serializer_class = EleicaoSerializer
    lookup_url_kwarg = 'codigo'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            codigo = request.GET.get(self.lookup_url_kwarg)
            queryset = Eleicao.objects.filter(codigo=codigo)
            if queryset.exists():
                eleicao = queryset[0]
                documento = request.data.get('documento_eleitor')
                eleitor = Eleitor.objects.filter(documento=documento).first()
                if eleitor.pode_votar == 1:
                    eleitor.pode_votar = 2
                    eleitor.save(update_fields=['pode_votar'])

                    numero = request.data.get('numero')
                    candidato = Candidato.objects.filter(numero=numero).first()
                    candidato.votos = candidato.votos + 1
                    candidato.save(update_fields=['votos'])

                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({'Bad Request': 'Eleitor ja votou'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                eleicao = Eleicao()
                eleicao.save()
                return Response(EleicaoSerializer(eleicao).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class ResultsEleicaoView(APIView):
    serializer_class = EleicaoSerializer
    lookup_url_kwarg = 'codigo'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            eleicao = Eleicao.objects.filter(codigo=code)
            if len(eleicao) > 0:
                eleicao = eleicao[0]
                candidatos = Candidato.objects.filter(eleicao=eleicao).all()
                data = []
                for candidato in candidatos:
                    data.append({"Candidato": candidato.nome, "Numero": candidato.numero, "Votos": candidato.votos})
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Eleicao nao encontrada': 'Codigo invalido .'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Codigo nao informado'}, status=status.HTTP_400_BAD_REQUEST)

