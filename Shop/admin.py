from django.contrib import admin

from .models import Products, UserProfile, ImgProduct, Category, BufBasket, ListOrders

admin.site.register(Products)
admin.site.register(ImgProduct)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(BufBasket)
admin.site.register(ListOrders)

# Register your models here.
