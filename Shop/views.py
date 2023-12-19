from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserRegistrationForm, UserProfileForm, BasketForm, ProductsForm, ImgProductForm
from .models import UserProfile, Products, ImgProduct, Category, BufBasket


# Create your views here.

def UserInfo(user):
    try:
        info = UserProfile.objects.get(id_user=user)
        return info
    except:
        return False


def index(request):
    category = Category.objects.all()
    products = Products.objects.all().order_by("-published_date")  # сортує по даті додавання
    product = products
    long = len(products)
    img = ImgProduct.objects.all()
    context = {
        "category": category,
        "img": img,
        "product": product,
        "i": 0,
        "long": long
    }
    return render(request, 'Shop/index.html', context=context)

def product(request, id=None):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        form = BasketForm(request.POST)
        # if not request.user:
        #     return render(request, 'Shop/product.html', context={"text": "Авторизуйтесь"})

        if form.is_valid() and request.user:
            bask = form.save(commit=False)
            bask.user = request.user
            bask.prod = product
            bask.save()

            imgs = ImgProduct.objects.filter(product=product.id)
            context = {
                "imgs": imgs,
                "product": product,
                'add': "Додано до кошика"
            }
            return render(request, 'Shop/product.html', context=context)


    imgs = ImgProduct.objects.filter(product=product.id)
    context = {
        "imgs": imgs,
        "product": product
    }
    return render(request, 'Shop/product.html', context=context)

def category(request, name=None, id=None):
    # is_admin = request.user.is_staff
    cat = get_object_or_404(Category, name=name)
    products = Products.objects.filter(category=cat.id).order_by("-published_date")  # сортує по даті додавання
    long = len(products)
    start = id
    id += 1
    if id > long:
        id = long
        start = id - 1
    product = products[start:id]

    category = Category.objects.all()
    context = {
        "name": name,
        "long": long,
        "product": product,
        "category": category,
        "i": id
    }
    return render(request, 'Shop/category.html', context=context)

def user(request):
    category = Category.objects.all()
    if request.method == "POST":
        prod = ProductsForm(request.POST, request.FILES)
        if prod.is_valid():
            produc = prod.save(commit=False)
            produc.published_date = timezone.now()
            produc.save()
            for img in request.FILES.getlist('img'):
                imgpost = ImgProduct(product=produc, img=img)
                imgpost.save()
            return index(request)

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
        basket2 = BufBasket.objects.filter(user=user)
        basket = []
        sum = 0
        for b in basket2:
            product = Products.objects.get(id=b.prod.id)
            all = b.quantity * product.price
            sum += all
            item = {
                'id': b.id,
                'user': b.user,
                'product_name': product.name,
                'quantity': b.quantity,
                'price': product.price,
                'all_price': all
            }
            basket.append(item)

        if UserInfo(user):
            info = UserInfo(user)
            form = UserRegistrationForm()
            context = {
                'category':category,
                'user': user,
                'info': info,
                'form': form,
                'basket': basket,
                'sum': sum
            }
            return render(request, 'Shop/user.html', context=context)


    return render(request, 'Shop/user.html')


def logout_view(request):
    logout(request)
    return redirect('index')

def basket_del(request, id=None):
    buf_basket_instance = BufBasket.objects.get(id=id)
    buf_basket_instance.delete()
    return redirect('user')

def page(request, id=None):
    category = Category.objects.all()
    products = Products.objects.all().order_by("-published_date")  # сортує по даті додавання
    long = len(products)
    start = id
    id += 1
    if id > long:
        id = long
        start = id - 1
    product = products[start:id]
    img = ImgProduct.objects.all()
    context = {
        "long": long,
        "i": id,
        "category": category,
        "img": img,
        "product": product
    }
    return render(request, 'Shop/index.html', context=context)
