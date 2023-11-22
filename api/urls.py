from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import ClienteViewSet, ContaViewSet, CartaoViewSet



router = SimpleRouter()

router.register('clientes', ClienteViewSet)
router.register('contas', ContaViewSet)
router.register('cartoes', CartaoViewSet)