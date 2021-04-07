from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from products.models import Product
from datetime import datetime
from .models import Order, OrderItem, ShippingAddress
from .serializers import OrderSerializer


class Index(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class Create(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data
        user = request.user

        orderItems = data['orderItems']
        if orderItems and len(orderItems) == 0:
            return Response(
                {'detail': 'No Order Items'}, status=HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice'],
        )

        ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country']
        )

        for item in orderItems:
            product = Product.objects.get(id=item['product'])
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=item['qty'],
                price=item['price'],
                image=product.image.url
            )
            product.countInStock -= orderItem.qty
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class Show(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        user = request.user
        if user.id == order.user.id or user.is_staff:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)

        return Response(
            {'datail': 'You are Not Authorized to See This Order'},
            status=HTTP_401_UNAUTHORIZED
        )


class Pay(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class Deliver(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class MyOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
