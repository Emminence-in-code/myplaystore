from django.contrib import admin
from .models import CustomUser, UploadedApp,UploadHistory


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UploadHistory)
admin.site.register(UploadedApp)