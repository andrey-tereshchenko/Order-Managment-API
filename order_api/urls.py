from rest_framework.routers import DefaultRouter
from django.urls import path, include
from order_api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(r'accounts', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]
