from django.contrib import admin
from .models import Gift, Profile

# class ProfileAdmin(admin.ModelAdmin):
#     ...
#     search_fields = (


# Register your models here.
admin.site.register(Gift)
admin.site.register(Profile)