# Generated by Django 3.0.8 on 2020-08-23 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200820_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]
