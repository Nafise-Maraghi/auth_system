import datetime
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.utils import timezone
from user.models import CustomUser, UsernameModel


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'dalal']
        extra_kwargs = {'password': {'write_only': True}, 'username': {'required': True}}

    def validate_username(self, value):
        try:
            username_obj = UsernameModel.objects.create(username=value, started_at=timezone.now())

        except:
            username_obj = UsernameModel.objects.get(username=value)

            if username_obj.ended_at and username_obj.ended_at + datetime.timedelta(days=15) > timezone.now():
                raise serializers.ValidationError("This username is currently unavailable")

            username_obj.started_at = timezone.now()
            username_obj.save()
        
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(SignUpSerializer, self).create(validated_data)


class ChangeUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']
    
    def validate_username(self, value):
        user = self.context['request'].user
        old_username = user.username
    
        if old_username:
            old_username_object = UsernameModel.objects.get(username=user.username)
            if old_username_object.started_at + datetime.timedelta(seconds=1) > timezone.now():
                raise serializers.ValidationError("You cannot change your username at the moment")

        try:
            username_obj = UsernameModel.objects.get(username=value)

        except:
            username_obj = None

        if username_obj:
            if username_obj.ended_at + datetime.timedelta(seconds=1) > timezone.now():
                raise serializers.ValidationError("This username is currently unavailable")
            
        return value
