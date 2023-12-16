from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile, Products, ImgProduct


# Create your views here.

def UserInfo(user):
    try:
        info = UserProfile.objects.get(id_user=user)
        return info
    except:
        return False


def index(request):
    product = Products.objects.all().order_by("-published_date")  # сортує по даті додавання
    img = ImgProduct.objects.all()
    context = {
        "img": img,
        "product": product
    }
    return render(request, 'Shop/index.html', context=context)

def product(request, id=None):
    product = get_object_or_404(Products, id=id)
    imgs = ImgProduct.objects.filter(product=product.id)
    context = {
        "imgs": imgs,
        "product": product
    }
    return render(request, 'Shop/product.html', context=context)





def user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Збереження користувача
            user = user_form.save()

            # Збереження профілю
            profile = profile_form.save(commit=False)
            profile.id_user = user
            profile.save()
            return render(request, 'Shop/user.html', context={"a": "Ви успішно зареєструвались"})

    if request.user.username:
        user = User.objects.get(username=request.user.username)
        if UserInfo(user):
            info = UserInfo(user)
            form = UserRegistrationForm()
            context = {
                'user': user,
                'info': info,
                'form': form
            }
            return render(request, 'Shop/user.html',context=context)


    return render(request, 'Shop/user.html')


def logout_view(request):
    logout(request)
    return redirect('index')