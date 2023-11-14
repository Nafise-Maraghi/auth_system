from rest_framework import serializers

from car.models import Car


class AddCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        obj = Car.objects.create(owner=self.context['request'].user, **validated_data)
        return obj


class ListCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
