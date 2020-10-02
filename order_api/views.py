from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from order_api.permission import IsAdminUser, IsLoggedInUserOrAdmin, \
    IsAdminOrCashier, IsAdminOrCashierOrSeller
from order_api.models import User, Product, Order, Account
from order_api.serializers import UserSerializer, ProductSerializer, \
    OrderSerializer, AccountSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsLoggedInUserOrAdmin]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_fields = {'status': ['exact'],
                     'order_creation_date': ['gte', 'lte', 'exact', 'gt', 'lt']}

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update':
            permission_classes = [IsAdminOrCashierOrSeller]
        else:
            permission_classes = [IsAdminOrCashier]

        return [permission() for permission in permission_classes]


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrCashier]
