from django.contrib import admin

# Register your models here.

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id')
    search_fields = ('user', 'id')
    list_filter = ('user', 'id')
    ordering = ('user', 'id')



