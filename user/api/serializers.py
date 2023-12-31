import datetime
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.utils import timezone
from user.models import CustomUser, UsernameModel, ChangeUsernameModel


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
    new_username = serializers.CharField(max_length=150)

    class Meta:
        model = CustomUser
        fields = ['new_username']

    def validate_new_username(self, value):
         # Check if the new username is already in use
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({"error":"This username is already in use."})

        # Check if the username was used in the past 15 days
        recent_use = ChangeUsernameModel.objects.filter(username=value, ended_at__gt=timezone.now() - datetime.timedelta(days=15)).exists()

        if recent_use:
            remaining_days = (ChangeUsernameModel.objects.get(username=value).ended_at - timezone.now()).days
            raise serializers.ValidationError({"error":f"This username cannot be used for another {remaining_days} days."})

        return value


# class ChangeUsernameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username']
    
#     def validate_username(self, value):
#         user = self.context['request'].user
#         old_username = user.username
    
#         if old_username:
#             old_username_object = UsernameModel.objects.get(username=user.username)
#             if old_username_object.started_at + datetime.timedelta(seconds=1) > timezone.now():
#                 raise serializers.ValidationError("You cannot change your username at the moment")

#         try:
#             username_obj = UsernameModel.objects.get(username=value)

#         except:
#             username_obj = None

#         if username_obj:
#             if username_obj.ended_at + datetime.timedelta(seconds=1) > timezone.now():
#                 raise serializers.ValidationError("This username is currently unavailable")
            
#         return value
        return value