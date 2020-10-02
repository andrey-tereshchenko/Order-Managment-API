# Generated by Django 3.1.1 on 2020-09-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NW', 'New order'), ('CM', 'Completed'), ('PD', 'Paid')], default='NW', max_length=2),
        ),
    ]
