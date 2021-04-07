from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer, UserSerializerWithToken


class Index(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class Update(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        user = request.user

        user.first_name = data['name']
        user.username = data['email']
        user.email = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])
        user.save()

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
