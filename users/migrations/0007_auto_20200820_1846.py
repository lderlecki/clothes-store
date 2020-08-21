# Generated by Django 3.0.8 on 2020-08-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='first_name',
            field=models.CharField(default='Default', max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(default='Default', max_length=100),
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default='500 600 700', max_length=100),
            preserve_default=False,
        ),
    ]
