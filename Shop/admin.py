from django.contrib import admin

from .models import Products, UserProfile, ImgProduct

admin.site.register(Products)
admin.site.register(ImgProduct)
admin.site.register(UserProfile)

# Register your models here.
