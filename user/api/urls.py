from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('signup/', custom_views.SignUpAPI.as_view(), name='signup'),
    path('login/', custom_views.LogInAPI.as_view(), name='login'),
]
