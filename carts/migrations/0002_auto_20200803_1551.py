# Generated by Django 3.0.8 on 2020-08-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='adress',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='delivery_price',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='price_total',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products_price',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='date_added',
        ),
        migrations.AddField(
            model_name='cart',
            name='completed',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_ordered',
            field=models.DateTimeField(),
        ),
    ]
