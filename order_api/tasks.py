from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import date
from order_api.models import Product


@shared_task
def make_discount_for_products():
    products = Product.objects.all()
    for product in products:
        delta_days = abs(product.creation_date - date.today()).days
        if delta_days > 30 and product.discount != 20:
            product.discount = 20
            product.save()
    print('Discount successful created')
