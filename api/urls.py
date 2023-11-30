from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import ClienteViewSet, ContaViewSet, CartaoViewSet, MovimentacaoViewSet, EmprestimoViewSet, AvaliacaoCreditoViewSet



router = SimpleRouter()

router.register('clientes', ClienteViewSet)
router.register('contas', ContaViewSet)
router.register('cartoes', CartaoViewSet)
router.register('movimentacao', MovimentacaoViewSet)
router.register('emprestimos', EmprestimoViewSet)
router.register('avaliacaoCredito', AvaliacaoCreditoViewSet)