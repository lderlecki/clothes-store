# Generated by Django 3.0.8 on 2020-08-31 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200831_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(blank=True, default='My address', max_length=100, null=True),
        ),
    ]
