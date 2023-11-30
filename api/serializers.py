from rest_framework import serializers

from django.db.models import Avg

from .models import ClienteConta, Conta, Cartao, Movimentacao, Emprestimo, AvaliacaoCredito
from django.contrib.auth.hashers import make_password

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:

        extra_kwargs = {
            'password': {'write_only':True} #NÃO VAI SER APRESENTADO QUANDO ALGUEM CONSULTAR, SERA EXIGIDO APENAS NO CADASTRO.
        }

        model = ClienteConta
        fields = (
            'id_cliente',
            'first_name',
            'last_name',
            'foto',
            'cpf',
            'dataNascimento',
            'username',
            'password',
            'telefone',
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
            'id_conta_destino',
            'valor',
            'dataMovimentacao',
            'tipo',
            'criacao',
            'atualizacao'
        )


class EmprestimoSerializer(serializers.ModelSerializer):

    class Meta:

        extra_kwargs = {
            'juros': {'read_only':True},
            'valor_parcela':{'read_only':True}
        }


        model = Emprestimo
        fields = (
            'id_emprestimo',
            'id_conta',
            'data_solicitacao',
            'valor_solicitado',
            'juros',
            'quantidade_parcelas',
            'valor_parcela',
            'data_aprovacao',
            'observacao',
            'criacao',
            'atualizacao'
        )
        
class AvaliacaoCreditoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvaliacaoCredito
        fields = (
            'id_conta',
            'limite',
            'permissao',
            'data_solicitacao'
        )