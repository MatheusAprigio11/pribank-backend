from rest_framework import serializers

from django.db.models import Avg

from .models import ClienteConta, Conta, Cartao, Movimentacao, Emprestimo, AvaliacaoCredito
from django.contrib.auth.hashers import make_password

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        print('meta')

        extra_kwargs = {
            'password': {'write_only':True} #NÃO VAI SER APRESENTADO QUANDO ALGUEM CONSULTAR, SERA EXIGIDO APENAS NO CADASTRO.
        }

        model = ClienteConta
        fields = '__all__'
        
        
    def create(self, validated_data):
        cliente = ClienteConta(
            foto = validated_data['foto'],
            cpf=validated_data['cpf'],
            password=validated_data['password'],
            dataNascimento = validated_data['dataNascimento'],
            telefone = validated_data['telefone'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        


        cliente.set_password(validated_data['password'])
        cliente.save()
        return cliente




class CartaoSerializer(serializers.ModelSerializer):
    

    class Meta:

        model = Cartao
        fields = (
            'id_cartao',
            'conta',
            'numero',
            'validade',
            'tipo',
            'limite',
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


class ContaSerializer(serializers.ModelSerializer):

    conta_cartao = CartaoSerializer(read_only=True)
    id_cliente = ClienteSerializer(read_only=True)

    class Meta:

        model = Conta
        fields = (
            'id_conta',
            'id_cliente',
            'conta_cartao',
            'agencia',
            'conta',
            'saldo',
            'ativa')