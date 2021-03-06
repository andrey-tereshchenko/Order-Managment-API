# Generated by Django 3.1.1 on 2020-10-01 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0003_auto_20201001_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_price',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='order_api.product'),
            preserve_default=False,
        ),
    ]
