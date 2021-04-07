from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.serializers import UserSerializer
from .models import Order, OrderItem, ShippingAddress


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    user = SerializerMethodField(read_only=True)
    orderItems = SerializerMethodField(read_only=True)
    shippingAddress = SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self, obj):
        serializer = UserSerializer(obj.user, many=False)
        return serializer.data

    def get_orderItems(self, obj):
        orderItems = obj.orderitem_set.all()
        serializer = OrderItemSerializer(orderItems, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            serializer = ShippingAddressSerializer(
                obj.shippingaddress, many=False
            )
            return serializer.data
        except ShippingAddress.DoesNotExist:
            return False
