from django.urls import path

# from . import views as custom_views
from .views import SignUpAPI, LogInAPI, ChangeUsernameAPI


urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('login/', LogInAPI.as_view(), name='login'),
    path('change_username/', ChangeUsernameAPI.as_view(), name='change_username'),
]
