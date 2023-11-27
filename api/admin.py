from django.contrib import admin

from .models import Cliente, Conta, Cartao, Movimentacao, Emprestimo

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'foto', 'dataNascimento', 'usuario', 'senha', 'telefone')

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
