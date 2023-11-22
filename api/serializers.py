from rest_framework import serializers

from django.db.models import Avg

from .models import Cliente, Conta, Cartao, Movimentacao, Emprestimo
from django.contrib.auth.hashers import make_password

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:

        extra_kwargs = {
            'senha': {'write_only':True} #NÃO VAI SER APRESENTADO QUANDO ALGUEM CONSULTAR, SERA EXIGIDO APENAS NO CADASTRO.
        }

        model = Cliente
        fields = (
            'id_cliente',
            'nome',
            'foto',
            'dataNascimento',
            'usuario',
            'senha',
            'telefone',
            'criacao',
            'atualizacao'
        )

class ContaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Conta
        fields = "__all__"


class CartaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cartao
        fields = (
            'id_cartao',
            'id_conta',
            'numero',
            'validade',
            'cvv',
            'bandeira',
            'situacao',
            'criacao',
            'atualizacao'
        )




class MovimentacaoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movimentacao
        fields = (
            'id_movimentacao',
            'id_cartao',
            'id_conta',
            'valor',
            'dataMovimentacao',
            'tipo',
            'criacao',
            'atualizacao'
        )


class EmprestimoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Emprestimo
        fields = (
            'id_emprestimo',
            'id_conta',
            'data_solicitacao',
            'valor_solicitado',
            'juros',
            'nuemro_parcela',
            'aprovado',
            'data_aprovaco',
            'observacao',
            'criacao',
            'atualizacao'
        )