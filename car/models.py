from django.db import models

from user.models import CustomUser


class Car(models.Model):
    manufacture_year = models.IntegerField()
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return self.name
        