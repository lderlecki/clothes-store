# Generated by Django 3.0.8 on 2020-08-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200820_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(default='Poland', max_length=100),
            preserve_default=False,
        ),
    ]