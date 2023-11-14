from django.urls import path, include

from .views import ProfileListAPI, ProfileDetailAPI, MyProfileAPI


urlpatterns = [
    path('profile/', ProfileListAPI.as_view(), name='profile_list'),
    path('profile/<int:pk>/', ProfileDetailAPI.as_view(), name='profile_detail'),
    path('me/', MyProfileAPI.as_view(), name='my_profile'),
]
