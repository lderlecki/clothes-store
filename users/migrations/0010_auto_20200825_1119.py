# Generated by Django 3.0.8 on 2020-08-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200824_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], default='S', max_length=1),
        ),
    ]
