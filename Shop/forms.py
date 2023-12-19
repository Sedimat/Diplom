from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Products, ImgProduct, UserProfile,BufBasket

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('id_user',)

class BasketForm(forms.ModelForm):
    class Meta:
        model = BufBasket
        exclude = ('user', 'prod',)

class ImgProductForm(forms.ModelForm):
    class Meta:
        model = ImgProduct
        exclude = ('product',)

class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ('published_date',)



