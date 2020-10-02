from rest_framework.serializers import ModelSerializer

from order_api.models import User, Product, Order, Account


class UserSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'username', 'password', 'groups',
            'email')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.save()

        return user


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'creation_date', 'discount')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ('order', 'account_creation_date')
