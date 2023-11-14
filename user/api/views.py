from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import CustomUser
from .serializers import SignUpSerializer


class SignUpAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer


class LogInAPI(APIView):
    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        print(email)
        print(password)
        user = authenticate(request=self.request ,email=email, password=password)

        print("###############")
        u = CustomUser.objects.get(email=email)
        print('email: ', u.email == email)
        print('password: ', u.password == password)
        print('user: ', user)
        print("###############")

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
