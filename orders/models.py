from django.db.models import Model, CharField, IntegerField, DecimalField,\
    DateTimeField, BooleanField, BigAutoField
from django.db.models.fields.related import OneToOneField, ForeignKey
from django.db.models.deletion import SET_NULL, CASCADE
from django.contrib.auth.models import User
from products.models import Product
from .apps import OrdersConfig


class Order(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    paymentMethod = CharField(max_length=200, null=True, blank=True)
    taxPrice = DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = BooleanField(default=False)
    isDelivered = BooleanField(default=False)
    paidAt = DateTimeField(auto_now_add=False, null=True, blank=True)
    deliveredAt = DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f'{self.user.email} - {self.createdAt}'
        except AttributeError:
            return f'Deleted User - {self.createdAt}'


class OrderItem(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    order = ForeignKey(Order, on_delete=SET_NULL, null=True, blank=True)
    name = CharField(max_length=200, null=True, blank=True)
    qty = IntegerField(null=True, blank=True, default=0)
    price = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        try:
            return f'{self.order.user.email} - {self.product.name} \
                - {self.qty}'
        except AttributeError:
            return f'Deleted User - {self.product.name} - {self.qty}'


class ShippingAddress(Model):
    order = OneToOneField(Order, on_delete=CASCADE, null=True, blank=True)
    address = CharField(max_length=200, null=True, blank=True)
    city = CharField(max_length=200, null=True, blank=True)
    postalCode = CharField(max_length=200, null=True, blank=True)
    country = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.city} - {self.address}'


OrdersConfig.default_auto_field = BigAutoField
