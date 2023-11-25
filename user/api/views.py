from datetime import timedelta

from django.contrib.auth import authenticate, login
from django.db.models import Max
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer, ChangeUsernameSerializer
from user.models import CustomUser, UsernameModel, ChangeUsernameModel


def username_changed(old_username, new_username):
    current_time = timezone.now()
    old_username_object = UsernameModel.objects.get(username=old_username)
    old_username_object.ended_at = current_time
    old_username_object.save()

    try:
        new_username_object = UsernameModel.objects.get(username=new_username)
        new_username_object.started_at = current_time
        new_username_object.save()
    
    except:
        new_username_object = UsernameModel.objects.create(username=new_username, started_at=current_time)


class SignUpAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer


class LogInAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request=request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangeUsernameView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Check if the user has changed username in the last 15 days
            last_change = ChangeUsernameModel.objects.filter(user=user).aggregate(last_change=Max('started_at')).get('last_change')

            # Check if this change was within the last 15 days
            if last_change and (timezone.now() - last_change) < timedelta(days=15):
                return Response(
                    {"error": "You can only change your username every 15 days."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save old username with a 15-day restriction
            ChangeUsernameModel.objects.create(
                user= user,
                username=user.username, 
                started_at=timezone.now(), 
                ended_at=timezone.now() + timedelta(days=15)
            )

            # Change username
            user.username = serializer.validated_data['new_username']
            user.save()

            return Response({"message": "Username changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ChangeUsernameAPI(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = CustomUser.objects.all()
#     serializer_class = ChangeUsernameSerializer

#     def get_object(self):
#         return CustomUser.objects.get(email=self.request.user)

#     def perform_update(self, serializer):
#         old_username = self.request.user.username
#         new_username = self.request.data.get('username')

#         if old_username == new_username:
#             return Response(status=status.HTTP_200_OK)

#         try:
#             username_changed(old_username=old_username, new_username=new_username)

#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         return super().perform_update(serializer)
