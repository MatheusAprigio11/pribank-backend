from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ClienteConta, Conta, Cartao, Movimentacao, Emprestimo

from .forms import ClienteCreateForm, ClienteChangeForm

@admin.register(ClienteConta)
class ClienteAdmin(UserAdmin):
    add_form = ClienteCreateForm
    form = ClienteChangeForm
    model = ClienteConta
    
    list_display = ('foto', 'first_name', 'last_name', 'cpf', 'dataNascimento','telefone', 'token')
    readonly_fields = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'cpf', 'dataNascimento', 'telefone')}),
        ('Permissões', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('date_joined',)}), 
    )

    list_filter = ('is_staff', 'is_superuser')

# @admin.register(ClienteConta)
# class ClienteAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'foto', 'dataNascimento', 'username', 'password', 'telefone')

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('agencia', 'conta', 'limite', 'ativa')

@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'validade', 'cvv', 'bandeira', 'situacao')

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('valor', 'dataMovimentacao', 'tipo')

@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('data_solicitacao', 'valor_solicitado', 'juros','quantidade_parcelas', 'valor_parcela', 'aprovado', 'data_aprovacao', 'observacao')
