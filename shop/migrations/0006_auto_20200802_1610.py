# Generated by Django 3.0.8 on 2020-08-02 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200801_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, default='product_placeholder.png', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='product_placeholder.png', null=True, upload_to=''),
        ),
    ]
