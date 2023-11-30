from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission


class ClienteManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('O e-mail é obrigatório')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(username, password, **extra_fields)
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super precisa ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super precisa ter is_staff=True')
        
        return self._create_user(username, password, **extra_fields)
        


class ClienteConta(AbstractUser):
    id_cliente = models.AutoField(primary_key=True)
    foto = models.ImageField(max_length=255)
    dataNascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=11)
    token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['foto', 'first_name', 'last_name', 'cpf', 'telefone', 'dataNascimento']

    groups = models.ManyToManyField(
        Group,
        related_name='clienteconta_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='clienteconta_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id_cliente']

    def __str__(self):
        return self.username
    
    objects = ClienteManager()


@receiver(post_save, sender=ClienteConta)
def create_token_for_user(sender, instance, created, **kwargs):
    if created:
        # Criar um usuário associado ao cliente
        user, created = ClienteConta.objects.get_or_create(username=instance.username)
        # Você pode definir uma senha padrão ou gerar uma senha aleatória aqui
        user.set_password(instance.password)
        user.save()

        # Criar ou obter um token para o usuário
        token, created = Token.objects.get_or_create(user=user)
        instance.token = token.key
        instance.save()
 


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Conta(Base):
    
    id_conta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(ClienteConta, related_name="conta_cliente", on_delete=models.CASCADE)
    agencia = models.IntegerField('Agencia')
    conta = models.CharField(max_length=10)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    ativa = models.BooleanField('Ativa?', default=True)
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['id_conta']


class Cartao(Base):
    
    TIPO_CHOICES = [
        ('CD/CC', 'Cartão de Débito e Crédito'),
        ('CD', 'Cartão de Débito')
    ]
    
    id_cartao = models.AutoField(primary_key=True)
    id_conta = models.ForeignKey(Conta, related_name='conta_cartao', on_delete=models.CASCADE)
    numero = models.CharField(max_length=16)
    validade = models.DateField()
    cvv = models.IntegerField()
    tipo = models.CharField('tipo', max_length=10, choices=TIPO_CHOICES, null=False)
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


class AvaliacaoCredito(models.Model):
    id_conta = models.ForeignKey(Conta, related_name="avaliacao_credito_conta",on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    permissao = models.BooleanField(blank=True, null=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Avaliacao Credito'
        verbose_name_plural = 'Avaliacoes Credito'