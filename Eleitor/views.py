from django.shortcuts import render
from RabbitMQ.rabbit import Rabbit
from rest_framework import generics, status
from .serializers import EleitorSerializer, CreateEleitorSerializer
from .models import Eleitor
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import json

# Create your views here.

class EleitorView(APIView):
    serializer_class = CreateEleitorSerializer
    lookup_url_kwarg = 'documento'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            eleitor = Eleitor.objects.filter(documento=code)
            if len(eleitor) > 0:
                data = EleitorSerializer(eleitor[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Eleitor nao encontrado': 'Documento invalido .'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            nome = serializer.data.get('nome')
            documento = serializer.data.get('documento')
            foto = serializer.data.get('foto')
            queryset = Eleitor.objects.filter(documento=documento)
            if queryset.exists():
                eleitor = queryset[0]
                eleitor.nome = nome
                eleitor.documento = documento
                eleitor.save(update_fields=['nome', 'documento'])
                return Response(EleitorSerializer(eleitor).data, status=status.HTTP_200_OK)
            else:
                eleitor = Eleitor(nome=nome, documento=documento, foto=foto)
                eleitor.save()
                return Response(EleitorSerializer(eleitor).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEleitorView(APIView):
    serializer_class = EleitorSerializer
    lookup_url_kwarg = 'documento'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            eleitor = Eleitor.objects.filter(documento=code)
            if len(eleitor) > 0:
                eleitor = eleitor[0]
                data = EleitorSerializer(eleitor).data
                pode_votar = data["pode_votar"]
                if pode_votar == 1:
                    eleitor.pode_votar = 2
                    eleitor.save(update_fields=['pode_votar'])
                    return Response(status=status.HTTP_200_OK)
                elif pode_votar == 2:
                    return Response({'Eleitor ja votou': 'So e possivel votar uma vez'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'Eleitor nao pode votar': 'Ainda nao foi aprovado pelo mesario'}, status=status.HTTP_401_UNAUTHORIZED)
                    
            return Response({'Eleitor nao encontrado': 'Documento invalido'}, status=status.
            HTTP_404_NOT_FOUND)
        
        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()  

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            documento = serializer.data.get('documento')
            queryset = Eleitor.objects.filter(documento=documento)
            if queryset.exists():
                rabbit = Rabbit()
                rabbit.produce(body=json.dumps(request.data))
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'Eleitor nao encontrado': 'Documento invalido .'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)      