from rest_framework import serializers

from user.models import CustomUser
from car.models import Car


# field are different in car/api/serializers
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'name', 'manufacture_year']


class ProfileSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'dalal', 'cars']

