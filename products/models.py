from django.db.models import Model, CharField, IntegerField, DecimalField, \
    TextField, DateTimeField, BigAutoField
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from .apps import ProductsConfig


class Product(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    name = CharField(max_length=200, null=True, blank=True)
    image = CloudinaryField(
        'image', null=True, blank=True, default='placeholder_y55v6h.png'
    )
    brand = CharField(max_length=200, null=True, blank=True)
    category = CharField(max_length=200, null=True, blank=True)
    description = TextField(null=True, blank=True)
    rating = DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = IntegerField(null=True, blank=True, default=0)
    price = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = IntegerField(null=True, blank=True, default=0)
    createdAt = DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Review(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    name = CharField(max_length=200, null=True, blank=True)
    rating = IntegerField(null=True, blank=True, default=0)
    comment = TextField(null=True, blank=True)
    createdAt = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'


ProductsConfig.default_auto_field = BigAutoField
