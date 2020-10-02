from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from order_api.models import User, Product, Order


class BaseTestCase(APITestCase):
    def setUp(self):
        self.group_admin = Group.objects.create(name='admin')
        self.group_cashier = Group.objects.create(name='cashier')
        self.group_seller = Group.objects.create(name='seller')
        self.group_accountant = Group.objects.create(name='accountant')
        self.admin = User.objects.create_superuser(username='admin',
                                                   email='admin@gmail.com',
                                                   password='admin',
                                                   groups_id=self.group_admin.id
                                                   )
        self.user_cashier = User.objects.create_user(
            username='user',
            email='user@gmail.com',
            password='user',
            groups_id=self.group_cashier.id)
        self.user_seller = User.objects.create_user(
            username='seller',
            email='seller@gmail.com',
            password='seller',
            groups_id=self.group_seller.id)
        self.user_accountant = User.objects.create_user(
            username='accountant',
            email='acc@gmail.com',
            password='accountant',
            groups_id=self.group_accountant.id
        )
        self.product_laptop = Product.objects.create(name='Acer aspire e151',
                                                     price=15000)
        self.product_smartphone = Product.objects.create(name='Iphone 7s',
                                                         price=8000)
        self.product_tv = Product.objects.create(name='Samsung Full HD',
                                                 price=28000)
        self.first_order = Order.objects.create(product=self.product_smartphone,
                                                order_creation_date='2020-05-11'
                                                )
        self.second_order = Order.objects.create(
            product=self.product_tv,
            order_creation_date='2020-07-14'
        )
        self.third_order = Order.objects.create(product=self.product_laptop)


class UserTestCase(BaseTestCase):

    def test_access_token(self):
        data = {"username": "admin",
                "password": "admin"}
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_by_admin(self):
        url = reverse('users-list')
        data = {'username': 'created_user',
                'password': 'created_user',
                'groups': self.group_cashier.id,
                'email': 'created_user@gmail.com'}
        token = AccessToken.for_user(self.admin)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_not_by_admin(self):
        url = reverse('users-list')
        data = {'username': 'created_user_1',
                'password': 'created_user_1',
                'groups': self.group_cashier.id,
                'email': 'created_user_1@gmail.com'}
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_by_admin(self):
        url = reverse('users-list')
        token = AccessToken.for_user(self.admin)
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_without_auth(self):
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_by_admin(self):
        url = reverse('users-detail', kwargs={'pk': self.user_cashier.id})
        data = {'username': 'updated_user',
                'password': 'updated_user',
                'groups': self.group_cashier.id,
                'email': 'updated_user@gmail.com'}
        token = AccessToken.for_user(self.admin)
        response = self.client.put(url, data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_own_record(self):
        url = reverse('users-detail', kwargs={'pk': self.user_cashier.id})
        data = {'username': 'own_updated_user',
                'password': 'own_updated_user',
                'groups': self.group_cashier.id,
                'email': 'updated_1_user@gmail.com'}
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.put(url, data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_another_record_by_seller(self):
        url = reverse('users-detail', kwargs={'pk': self.user_cashier.id})
        data = {'username': 'updated_seller',
                'password': 'updated_seller',
                'groups': self.group_cashier.id,
                'email': 'updated_seller@gmail.com'}
        token = AccessToken.for_user(self.user_seller)
        response = self.client.put(url, data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(
                                       token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_user_by_admin(self):
        url = reverse('users-detail', kwargs={'pk': self.user_cashier.id})
        data = {'username': 'partial_updated_user'}
        token = AccessToken.for_user(self.admin)
        response = self.client.patch(url, data,
                                     HTTP_AUTHORIZATION='Bearer {}'.format(
                                         token))
        current_user = User.objects.filter(id=self.user_cashier.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_user.username, data['username'])

    def test_retrieve_own_record(self):
        url = reverse('users-detail', kwargs={'pk': self.user_cashier.id})
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.get(url, HTTP_AUTHORIZATION='Bearer {}'.format(
            token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductTestCase(BaseTestCase):

    def test_create_product_by_admin(self):
        url = reverse('products-list')
        data = {'name': 'Iphone X',
                'price': '24000'}
        token = AccessToken.for_user(self.admin)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_by_no_authorization_user(self):
        url = reverse('products-list')
        data = {'name': 'Iphone X',
                'price': '24000'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_by_no_admin_user(self):
        url = reverse('products-list')
        data = {'name': 'Iphone X',
                'price': '24000'}
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_product_by_authorization_user(self):
        url = reverse('products-list')
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_product_by_no_authorization_user(self):
        url = reverse('products-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_product_by_admin(self):
        url = reverse('products-detail', kwargs={'pk': self.product_laptop.id})
        data = {'name': 'Lenovo g500',
                'price': '14000'}
        token = AccessToken.for_user(self.admin)
        response = self.client.put(url, data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_by_no_admin(self):
        url = reverse('products-detail', kwargs={'pk': self.product_laptop.id})
        data = {'name': 'Lenovo g501',
                'price': '14000'}
        token = AccessToken.for_user(self.user_seller)
        response = self.client.put(url, data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_retrieve_by_admin(self):
        url = reverse('products-detail', kwargs={'pk': self.product_laptop.id})
        token = AccessToken.for_user(self.admin)
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_delete_by_admin(self):
        url = reverse('products-detail', kwargs={'pk': self.product_laptop.id})
        token = AccessToken.for_user(self.admin)
        response = self.client.delete(url,
                                      HTTP_AUTHORIZATION='Bearer {}'.format(
                                          token)
                                      )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderTestCase(BaseTestCase):

    def test_create_order_by_admin(self):
        url = reverse('orders-list')
        data = {'product': self.product_tv.id}
        token = AccessToken.for_user(self.admin)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_by_cashier(self):
        url = reverse('orders-list')
        data = {'product': self.product_tv.id}
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_by_seller(self):
        url = reverse('orders-list')
        data = {'product': self.product_tv.id}
        token = AccessToken.for_user(self.user_seller)
        response = self.client.post(url, data,
                                    HTTP_AUTHORIZATION='Bearer {}'.format(
                                        token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_orders_by_cashier(self):
        url = reverse('orders-list')
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.get(url,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_new_orders_by_seller(self):
        url = reverse('orders-list')
        status_filter = '?status=NW'
        token = AccessToken.for_user(self.user_seller)
        response = self.client.get(url + status_filter,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_orders_filter_date_range_by_accountant(self):
        url = reverse('orders-list')
        start_date = '2020-06-01'
        end_date = '2020-10-04'
        status_filter = '?order_creation_date__gte={}' \
                        '&order_creation_date__lte={}'.format(start_date,
                                                              end_date)
        token = AccessToken.for_user(self.user_accountant)
        response = self.client.get(url + status_filter,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_operate_order_by_seller(self):
        url = reverse('orders-detail', kwargs={'pk': self.first_order.id})
        data = {'status': 'CM'}
        token = AccessToken.for_user(self.user_seller)
        response = self.client.patch(url, data,
                                     HTTP_AUTHORIZATION='Bearer {}'.format(
                                         token))
        current_order = Order.objects.filter(id=self.first_order.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_order.status, data['status'])

    def test_get_pay_order_by_cashier(self):
        url = reverse('orders-detail', kwargs={'pk': self.first_order.id})
        data = {'status': 'PD'}
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.patch(url, data,
                                     HTTP_AUTHORIZATION='Bearer {}'.format(
                                         token))
        current_order = Order.objects.filter(id=self.first_order.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(current_order.status, data['status'])

    def test_delete_order_by_cashier(self):
        url = reverse('orders-detail', kwargs={'pk': self.first_order.id})
        token = AccessToken.for_user(self.user_cashier)
        response = self.client.delete(url,
                                      HTTP_AUTHORIZATION='Bearer {}'.format(
                                          token))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
