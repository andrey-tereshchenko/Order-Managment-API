from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)

    REQUIRED_FIELDS = ['groups_id', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    creation_date = models.DateField(default=date.today)
    discount = models.IntegerField(default=0)


class Status(models.TextChoices):
    NEW = 'NW', 'New order'
    COMPLETED = 'CM', 'Completed'
    PAID = 'PD', 'Paid'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order_creation_date = models.DateField(default=date.today)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NEW,
    )


class Account(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    account_creation_date = models.DateField(default=date.today)
