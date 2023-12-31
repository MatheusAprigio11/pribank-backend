from django.shortcuts import render
from django.db.models import Q

from .models import ClienteConta, Cartao, Conta, Emprestimo, Movimentacao, AvaliacaoCredito
from .serializers import ClienteSerializer, CartaoSerializer, ContaSerializer, EmprestimoSerializer, MovimentacaoSerializer, AvaliacaoCreditoSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from rest_framework.views import APIView


# Create your views here.




class ClienteViewSet(viewsets.ModelViewSet):
    queryset = ClienteConta.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print('olaaa')
        cliente = request.data
        serializer = self.get_serializer(data=cliente)
        serializer.is_valid(raise_exception=True)

       
        try:
       
            cliente = serializer.save()
            
            print(cliente)

            conta = Conta(id_cliente=ClienteConta.objects.get(id_cliente=cliente.id_cliente),
                    agencia=random.randint(1000,9999),
                    conta=random.randint(10000000, 99999999),
                    saldo=1000.00)
            
            conta.save()

            fuso_horario = pytz.utc
            delta = relativedelta(years=5)
            data_criado = datetime.now(tz=fuso_horario)
            data_validade = data_criado + delta

            cartao = Cartao(conta=Conta.objects.get(id_conta=conta.id_conta),
                        numero=random.randint(1000000000000000,9000000000000000),
                        validade=data_validade,
                        tipo="CD",
                        limite='0.00',
                        cvv=random.randint(100,999),
                        bandeira="Mastercard"
                    )
            
            cartao.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ClienteContaView(viewsets.ModelViewSet):
    queryset = ClienteConta.objects.all()
    serializer_class = ClienteSerializer
    
    def get_queryset(self):
        cliente_destino = self.request.query_params.get('search')
        if cliente_destino:
            filters = ClienteConta.objects.filter(Q(cpf__icontains=cliente_destino)).distinct()
            return filters


class MovimentacaoViewSet(viewsets.ModelViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        dados_movimentacao = request.data
        cliente = ClienteConta.objects.filter(cpf=dados_movimentacao["cpf"]).first()
        print(cliente)
        conta = Conta.objects.filter(id_cliente=cliente).first()
        print(conta.id_conta)
        
        user = self.request.user
        print(user)
        
        if conta:
            movimentacao = Movimentacao(
                valor = Decimal(dados_movimentacao['valor']),
                tipo = dados_movimentacao['tipo']
            )

            if movimentacao.id_cartao is not None:
                print("entrou no primeiro if")
                movimentacao.id_cartao = dados_movimentacao['id_cartao']
            
            movimentacao.id_conta = Conta.objects.get(id_cliente=user)
            movimentacao.id_conta_destino = conta

            if movimentacao.valor >= movimentacao.id_conta.saldo:
                print('bad rqs')
                return Response({"message": "saldo insuficiente"},status=status.HTTP_400_BAD_REQUEST)
        
            print("caiu no if de movimentar o saldo")
            movimentacao.id_conta.saldo -=  movimentacao.valor
            movimentacao.id_conta_destino.saldo +=  movimentacao.valor
                
            movimentacaoSerializer = MovimentacaoSerializer(data=movimentacao)
            movimentacao.save()
            movimentacao.id_conta.save()
            movimentacao.id_conta_destino.save()    
            print('retorno')
            return Response(MovimentacaoSerializer(movimentacao).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
    def get_queryset(self):
        conta = Conta.objects.filter(id_cliente=self.request.user).first()
        
        movimentacao = Movimentacao.objects.filter(id_conta=conta)
        print(movimentacao)
        if movimentacao:
            return movimentacao
        else: 
            raise ValidationError(detail='Não existe movimentação nessa conta')
    
    
class CartaoViewSet(viewsets.ModelViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer


class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    
    
    def get_queryset(self):
        cliente = ClienteConta.objects.filter(cpf=self.request.user.cpf).first()
        conta = Conta.objects.filter(id_cliente=cliente).first()
        print(cliente.id_cliente)
        if cliente:
            return [conta]
        else: 
            raise ValidationError(detail='Esse cliente não existe')


class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    def create(self, request, *args, **kwargs):
        dados_emprestimo = request.data

        emprestimo = Emprestimo(
            id_conta=Conta.objects.get(id_conta=dados_emprestimo['id_conta']),
            valor_solicitado=Decimal(dados_emprestimo['valor_solicitado']),
            quantidade_parcelas=int(dados_emprestimo['quantidade_parcelas']),
            observacao=dados_emprestimo['observacao']
        )

        if emprestimo.valor_solicitado >= 15 * emprestimo.id_conta.saldo:
            return Response({"message": "Valor do empréstimo excede o saldo disponível."}, status=status.HTTP_400_BAD_REQUEST)

        self._calcular_juros(emprestimo)

        emprestimo.aprovado = True
        emprestimo.save()

        return Response(EmprestimoSerializer(emprestimo).data, status=status.HTTP_200_OK)

    def _calcular_juros(self, emprestimo):
        if emprestimo.quantidade_parcelas <= 12:
            emprestimo.juros = Decimal(0.10)
        elif emprestimo.quantidade_parcelas <= 24:
            emprestimo.juros = Decimal(0.15)
        elif emprestimo.quantidade_parcelas <= 36:
            emprestimo.juros = Decimal(0.20)

        parcela = emprestimo.valor_solicitado / emprestimo.quantidade_parcelas
        juros_parcela = parcela * emprestimo.juros
        emprestimo.valor_parcela = parcela + juros_parcela
        
        

    
        
        
class AvaliacaoCreditoViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoCredito.objects.all() #IMPORTAR DO MODELS
    serializer_class = AvaliacaoCreditoSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            avaliacao = serializer.validated_data
            conta = avaliacao['id_conta']
            cartao = conta.conta_cartao
            saldo = conta.saldo
            
            self.avaliar_credito(saldo, conta, cartao)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def avaliar_credito(self, saldo, conta, cartao):
        if saldo >= 500.00:
            limite = 0.5*float(saldo)
            cartao.limite = limite
            cartao.tipo = 'CD/CC'
            cartao.save()
            
            AvaliacaoCredito.objects.create(id_conta=conta, limite=limite, permissao=True)

        else:
            cartao.limite = 0.00
            cartao.save()
            AvaliacaoCredito.objects.create(id_conta=conta, limite=0.00, permissao=False)
            