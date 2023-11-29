from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cliente(Base):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    foto = models.CharField(max_length=255)
    dataNascimento = models.DateField()
    usuario = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=30)
    telefone = models.CharField(max_length=11, unique=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id_cliente']

    def __str__(self):
        return self.nome

@receiver(post_save, sender=Cliente)
def create_token_for_user(sender, instance, created, **kwargs):
    if created:
        # Criar um usuário associado ao cliente
        user, created = User.objects.get_or_create(username=instance.usuario)
        # Você pode definir uma senha padrão ou gerar uma senha aleatória aqui
        user.set_password(instance.senha)
        user.save()

        # Criar ou obter um token para o usuário
        token, created = Token.objects.get_or_create(user=user)
        instance.token = token.key
        instance.save()   


class Conta(Base):
    id_conta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, related_name="conta_cliente", on_delete=models.CASCADE)
    agencia = models.IntegerField('Agencia')
    conta = models.CharField(max_length=10)
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    ativa = models.BooleanField('Ativa?', default=True)
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['id_conta']


class Cartao(Base):
    id_cartao = models.AutoField(primary_key=True)
    id_conta = models.ForeignKey(Conta, related_name='conta_cartao', on_delete=models.CASCADE)
    numero = models.CharField(max_length=16)
    validade = models.DateField()
    cvv = models.IntegerField()
    bandeira = models.CharField(max_length=15)
    situacao = models.BooleanField('Ativo?', default=True)

    class Meta:
        verbose_name = 'Cartao'
        verbose_name_plural = 'Cartoes'
        ordering = ['id_cartao']


class Movimentacao(Base):
    id_movimentacao = models.AutoField(primary_key=True)
    id_cartao = models.ForeignKey(Cartao, related_name='movimentacoes_cartao', on_delete=models.CASCADE, null=True, blank=True)
    id_conta = models.ForeignKey(Conta, related_name='movimentacoes_conta', on_delete=models.CASCADE)
    id_conta_destino = models.ForeignKey(Conta, related_name='movimentacao_destino', on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dataMovimentacao = models.DateField(auto_now=True)
    tipo = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Movimentacao'
        verbose_name_plural = 'Movimentacoes'
        ordering = ['id_movimentacao']

class Emprestimo(Base):
    id_emprestimo = models.AutoField(primary_key=True)
    id_conta = models.ForeignKey(Conta, related_name="emprestimo_conta",on_delete=models.CASCADE)
    data_solicitacao = models.DateField(auto_now_add=True)
    valor_solicitado = models.DecimalField(max_digits=10, decimal_places=2)
    juros = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_parcelas = models.IntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    aprovado = models.BooleanField()
    data_aprovacao = models.DateField(auto_now_add=True)
    observacao = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = ['id_emprestimo']

        