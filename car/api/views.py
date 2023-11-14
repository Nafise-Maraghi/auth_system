from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from .serializers import AddCarSerializer, ListCarSerializer
from car.models import Car


class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You have reached yout limit'


class AddCarAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()
    serializer_class = AddCarSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        
        if user.dalal:
            limit = 30
        
        else:
            limit = 1

        if user.cars.count() < limit:
            return super().create(request, *args, **kwargs)
        
        else:
            raise CustomValidation()


class ListCarAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Car.objects.all()
    serializer_class = ListCarSerializer
