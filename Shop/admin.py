from django.contrib import admin

from .models import Products, UserProfile, ImgProduct, Category

admin.site.register(Products)
admin.site.register(ImgProduct)
admin.site.register(UserProfile)
admin.site.register(Category)

# Register your models here.
