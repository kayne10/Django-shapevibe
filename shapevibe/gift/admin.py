from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Gift, Profile

# class ProfileAdmin(admin.ModelAdmin):
#     ...
#     search_fields = (




# Register your models here.
admin.site.register(Gift)
admin.site.register(Profile)
admin.site.site_header = 'Shapevibe Administration'
admin.site.site_title = 'Shapevibe'