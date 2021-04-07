from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, UserSerializerWithToken


class Index(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class Create(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                first_name=data.get('name'),
                username=data.get('email'),
                email=data.get('email'),
                password=make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except IntegrityError:
            message = {'data': 'User With This Email is Already Exist'}
            return Response(message, status=HTTP_400_BAD_REQUEST)


class Show(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class Update(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        data = request.data
        user = get_object_or_404(User, id=pk)

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']
        user.is_staff = data['isAdmin']
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class Delete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response('User Deleted Succussfully')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop('access')
        data.pop('refresh')

        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
