from django.shortcuts import render

from .models import Cliente, Cartao, Conta, Emprestimo, Movimentacao
from .serializers import ClienteSerializer, CartaoSerializer, ContaSerializer, EmprestimoSerializer, MovimentacaoSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response

import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        dados_cliente = request.data
        cliente = Cliente(nome=dados_cliente['nome'],
                          foto=dados_cliente['foto'],
                          dataNascimento=dados_cliente['dataNascimento'],
                          usuario=dados_cliente['usuario'],
                          senha=dados_cliente['senha'],
                          telefone=dados_cliente['telefone'])

       
        clienteSerializer = ClienteSerializer(many=True, data=dados_cliente)

        if clienteSerializer.is_valid():

            cliente.save()

            conta = Conta(id_cliente=Cliente.objects.get(id_cliente=cliente.id_cliente),
                      agencia=random.randint(1000,9000),
                      conta=random.randint(10000000, 90000000),
                      limite=200.00)
            
            conta.save()

            fuso_horario = pytz.utc
            delta = relativedelta(years=5)
            data_criado = datetime.now(tz=fuso_horario)
            data_validade = data_criado + delta

            cartao = Cartao(id_conta=Conta.objects.get(id_conta=conta.id_conta),
                        numero=random.randint(1000000000000000,9000000000000000),
                        validade=data_validade,
                        cvv=random.randint(100,999),
                        bandeira="Mastercard"
                    )
            
            cartao.save()

            return Response(data=clienteSerializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CartaoViewSet(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer


class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer


class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer


class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer



    #  cartao = Cartao(numero=random.randint(1000000000000000,9000000000000000),
    #                     id_conta=
    #                     validade=data_criado + delta,
    #                     bandeira="Mastercard")
    # fuso_horario = pytz.utc
    #     delta = timedelta(year=5)
    #     data_criado = datetime.now(tz=fuso_horario)