from django.shortcuts import render

from .models import ClienteConta, Cartao, Conta, Emprestimo, Movimentacao
from .serializers import ClienteSerializer, CartaoSerializer, ContaSerializer, EmprestimoSerializer, MovimentacaoSerializer, AvaliacaoCreditoSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response


import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from decimal import Decimal

# Create your views here.

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = ClienteConta.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        cliente = request.data
        serializer = self.get_serializer(data=cliente)
        serializer.is_valid(raise_exception=True)

       
        try:
       
            cliente = serializer.save()
            
            print(cliente)

            conta = Conta(id_cliente=ClienteConta.objects.get(id_cliente=cliente.id_cliente),
                    agencia=random.randint(1000,9000),
                    conta=random.randint(10000000, 90000000),
                    saldo=200.00)
            
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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        dados_movimentacao = request.data

        movimentacao = Movimentacao(
            valor = Decimal(dados_movimentacao['valor']),
            tipo = dados_movimentacao['tipo']
        )

        if movimentacao.id_cartao is not None:
            print("entrou no primeiro if")
            movimentacao.id_cartao = dados_movimentacao['id_cartao']
            movimentacao.id_conta = None
            movimentacao.id_conta_destino = None
        else:
            print("entrou no else")
            movimentacao.id_conta = Conta.objects.get(id_conta=dados_movimentacao['id_conta'])
            movimentacao.id_conta_destino = Conta.objects.get(id_conta=dados_movimentacao['id_conta_destino'])

            if movimentacao.valor >= movimentacao.id_conta.saldo:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                print("caiu no if de movimentar o saldo")
                movimentacao.id_conta.saldo -=  movimentacao.valor
                movimentacao.id_conta_destino.saldo +=  movimentacao.valor

            
        movimentacaoSerializer = MovimentacaoSerializer(data=dados_movimentacao)
        if movimentacaoSerializer.is_valid():
            movimentacao.save()
            movimentacao.id_conta.save()
            movimentacao.id_conta_destino.save()    
            return Response(status=status.HTTP_200_OK)
        

class CartaoViewSet(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer


class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer


class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    def create(self, request, *args, **kwargs):
        dados_emprestimo = request.data

        emprestimo = Emprestimo(
            id_conta=Conta.objects.get(id_conta=dados_emprestimo['id_conta']),
            valor_solicitado = Decimal(dados_emprestimo['valor_solicitado']),
            quantidade_parcelas = int(dados_emprestimo['quantidade_parcelas']),
            observacao = dados_emprestimo['observacao']
        )

        if emprestimo.valor_solicitado >= 150*emprestimo.id_conta.saldo:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            emprestimo.id_conta.saldo += emprestimo.valor_solicitado
            if emprestimo.quantidade_parcelas <= 12:
                emprestimo.juros = Decimal(0.10)
                
            elif emprestimo.quantidade_parcelas <= 24:
                emprestimo.juros = Decimal(0.15)

            elif emprestimo.quantidade_parcelas <= 36:
                emprestimo.juros = Decimal(0.20)
                
        parcela = emprestimo.valor_solicitado/emprestimo.quantidade_parcelas

        juros_parcela = parcela*emprestimo.juros
        juros_parcela += parcela

        emprestimo.valor_parcela = juros_parcela
        emprestimo.aprovado = True
        
        emprestimoSerializer = EmprestimoSerializer(data=dados_emprestimo)

        if emprestimoSerializer.is_valid():
            emprestimo.save()
            emprestimo.id_conta.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class AvaliacaoCreditoViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoCreditoSerializer.objects.all() #IMPORTAR DO MODELS
    serializer_class = AvaliacaoCreditoSerializer
    
    def create(self, request, *args, **kwargs):
        avaliacao = request.data
        serializer = self.get_serializer(data=avaliacao)
        serializer.is_valid(raise_exception=True)
        
        try:
            avaliacaoCred = serializer.validated_data
            conta = avaliacaoCred['id_conta']
            cartao = conta.id_cartao
            saldo = conta.id_cliente.saldo
            
            self.avaliar_credito(saldo, conta, cartao)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def avaliar_credito(self, saldo, conta, cartao):
        if saldo >= 500.00:
            limite = 0.5*float(saldo)
            cartao.limite = limite
            cartao.tipo = 'CD/CC'
            cartao.save()
            
            AvaliacaoCreditoSerializer.objects.create(conta=conta, limite=limite, permissao=True)

        else:
            cartao.limite = 0.00
            cartao.save()
            AvaliacaoCreditoSerializer.objects.create(conta=conta, limite=0.00, permissao=False)