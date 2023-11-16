from django.contrib import admin

from .models import CustomUser, UsernameModel


admin.site.register(CustomUser)


@admin.register(UsernameModel)
class UsernameAdmin(admin.ModelAdmin):
    fields  = ['username', 'started_at', 'ended_at']
