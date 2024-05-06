from django.shortcuts import render
from Eleitor.models import Eleitor
from Eleitor.serializers import EleitorSerializer
from rest_framework import generics, status
from .serializers import MesarioSerializer, CreateMesarioSerializer
from .models import Mesario
from RabbitMQ.rabbit import Rabbit
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

class MesarioView(APIView):
    serializer_class = CreateMesarioSerializer
    lookup_url_kwarg = 'documento'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            mesario = Mesario.objects.filter(documento=code)
            if len(mesario) > 0:
                data = MesarioSerializer(mesario[0]).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Mesario nao encontrado': 'Documento invalido .'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()


        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            nome = serializer.data.get('nome')
            documento = serializer.data.get('documento')
            queryset = Mesario.objects.filter(documento=documento)
            if queryset.exists():
                mesario = queryset[0]
                mesario.nome = nome
                mesario.documento = documento
                mesario.save(update_fields=['nome', 'numero'])
                return Response(MesarioSerializer(mesario).data, status=status.HTTP_200_OK)
            else:
                mesario = Mesario(nome=nome, documento=documento)
                mesario.save()
                return Response(MesarioSerializer(mesario).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyMesarioView(APIView):
    serializer_class = MesarioSerializer

    def get(self, request, format=None):
        rabbit = Rabbit()
        body = rabbit.consume()
        code = body['documento']
        if code != None:
            eleitor = Eleitor.objects.filter(documento=code)
            if len(eleitor) > 0:
                eleitor = eleitor[0]
                data = EleitorSerializer(eleitor).data
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Eleitor nao encontrado': 'Documento invalido'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)

class ApproveMesarioView(APIView):
    serializer_class = EleitorSerializer


    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data.get('documento')
            if code != None:
                eleitor = Eleitor.objects.filter(documento=code)
                if len(eleitor) > 0:
                    eleitor = eleitor[0]
                    eleitor.pode_votar = 1
                    eleitor.save(update_fields=['pode_votar'])
                    data = EleitorSerializer(eleitor).data
                    return Response(data, status=status.HTTP_200_OK)
                return Response({'Eleitor nao encontrado': 'Documento invalido'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)

class DenyMesarioView(APIView):
    serializer_class = EleitorSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data.get('documento')
            if code != None:
                eleitor = Eleitor.objects.filter(documento=code)
                if len(eleitor) > 0:
                    eleitor = eleitor[0]
                    eleitor.pode_votar = 0
                    eleitor.save(update_fields=['pode_votar'])
                    data = EleitorSerializer(eleitor).data
                    return Response(data, status=status.HTTP_200_OK)
                return Response({'Eleitor nao encontrado': 'Documento invalido'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Documento nao informado'}, status=status.HTTP_400_BAD_REQUEST)