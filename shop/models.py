from django.db import models
from django.utils import timezone

# Create your models here.

PRODUCTS_GENDER = [
    ('woman', 'Woman'),
    ('man', 'Man'),
]

PRODUCTS_AGE = [
    ('adult', 'Adult'),
    ('kid', 'Kid'),
]


def get_image_path(instance, filename):
    id = instance.product.id
    return f'images/products/{id}/{filename}'


def get_image_preview(instance, filename):
    id = instance.id
    return f'images/products/{id}/preview_{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Category Name')
    image = models.ImageField(default='product_placeholder.png', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_man_categories(self):
        cat = self.pr


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Brand Name')
    image = models.ImageField(default='product_placeholder.png', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, choices=PRODUCTS_GENDER)
    age = models.CharField(max_length=20, null=True, choices=PRODUCTS_AGE)
    description = models.CharField(max_length=500, null=True, verbose_name='Description')
    net_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00, verbose_name='Net Price')
    vat = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='VAT', default=0.23)
    active = models.BooleanField(default=True, verbose_name='Is Active')
    image_preview = models.ImageField(upload_to=get_image_preview,
                                      default='product_placeholder.png',
                                      null=True, blank=True)
    date_created = models.DateTimeField(editable=False)
    date_modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        return round(self.net_price * (self.vat + 1), 2)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='product_images')
    image = models.ImageField(upload_to=get_image_path, verbose_name='Image')
