from django.urls import path, include

from .views import AddCarAPI, ListCarAPI


urlpatterns = [
    path('add/', AddCarAPI.as_view(), name='add_car'),
    path('list/', ListCarAPI.as_view(), name='list_car')
]
