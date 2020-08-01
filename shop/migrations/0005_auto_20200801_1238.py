# Generated by Django 3.0.8 on 2020-08-01 12:38

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_image_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_preview',
            field=models.ImageField(blank=True, default='product_placeholder.png', null=True, upload_to=shop.models.get_image_preview),
        ),
        migrations.AlterField(
            model_name='product',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=0.23, max_digits=100, verbose_name='VAT'),
        ),
    ]
