from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import CustomUser
from .serializers import ProfileSerializer


class ProfileListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetailAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'


class MyProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = CustomUser.objects.get(pk=request.user.pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
