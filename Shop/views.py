import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserRegistrationForm, UserProfileForm, BasketForm, ProductsForm, ImgProductForm
from .models import UserProfile, Products, ImgProduct, Category, BufBasket, ListOrders


# Create your views here.
def UpdateOrder(orders):
    list_orders = []
    for i in orders:
        a = json.loads(i.description)
        for it in a:
            product = get_object_or_404(Products, id=it[4])
            imgs = ImgProduct.objects.filter(product=product.id)
            user = User.objects.get(username=i.user)
            user_profile = UserProfile.objects.get(id_user=user.id)
            it.append(imgs[0])
            it.append(product)
        list_orders.append([i.user, a, i.status, i.date, i.price, user_profile, i.id])
    return list_orders

def ListOrder():
    new = ListOrders.objects.filter(status=1)
    work = ListOrders.objects.filter(status=2)
    end = ListOrders.objects.filter(status=3)
    return {'new': new, 'work': work, 'end': end, 'lnew': len(new), 'lwork': len(work), 'lend': len(end)}


def UserInfo(user):
    try:
        info = UserProfile.objects.get(id_user=user)
        return info
    except:
        return False

def BasketDict(user):
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
    return (basket,sum,)

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
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo(user)
        basket = BasketDict(user)
        Uinfo = {
            "basket": len(basket[0]),
            "sum": basket[1],
            "user": user,
            "userinfo": userinfo
            }
        context.update(Uinfo)
    return render(request, 'Shop/index.html', context=context)


def product(request, id=None):
    product = get_object_or_404(Products, id=id)
    imgs = ImgProduct.objects.filter(product=product.id)
    category = Category.objects.all()
    if request.method == "POST":
        form = BasketForm(request.POST)
        if form.is_valid() and request.user:
            bask = form.save(commit=False)
            bask.user = request.user
            bask.prod = product
            bask.save()
            return redirect('product', id=id)

    context = {
        "category": category,
        "imgs": imgs,
        "product": product
    }
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo(user)
        basket = BasketDict(user)
        Uinfo = {
            "basket": len(basket[0]),
            "sum": basket[1],
            "user": user,
            "userinfo": userinfo
            }
        context.update(Uinfo)

    return render(request, 'Shop/product.html', context=context)


def category(request, name=None, id=None):
    cat = get_object_or_404(Category, name=name)
    products = Products.objects.filter(category=cat.id).order_by("-published_date")  # сортує по даті додавання
    long = len(products)
    start = id
    id += 10
    if id > long:
        id = long
        start = id - (id % 10)
    product = products[start:id]

    category = Category.objects.all()
    context = {
        "name": name,
        "long": long,
        "product": product,
        "category": category,
        "i": id
    }
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo(user)
        basket = BasketDict(user)
        Uinfo = {
            "basket": len(basket[0]),
            "sum": basket[1],
            "user": user,
            "userinfo": userinfo
            }
        context.update(Uinfo)
    return render(request, 'Shop/category.html', context=context)


def user(request):
    category = Category.objects.all()
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
        orders = ListOrders.objects.filter(user=user).order_by("-date")
        list_orders = UpdateOrder(orders) # Перетворений список
        basket_buf = BasketDict(user)

        if UserInfo(user):
            info = UserInfo(user)
            form = UserRegistrationForm()
            context = {
                'orders': list_orders,
                'category': category,
                'user': user,
                'info': info,
                'form': form,
                'basket': basket_buf[0],
                'sum': basket_buf[1]
            }
            context.update(ListOrder())

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
    id += 12
    if id > long:
        id = long
        start = id - (id % 12)
    product = products[start:id]
    img = ImgProduct.objects.all()
    context = {
        "long": long,
        "i": id,
        "category": category,
        "img": img,
        "product": product
    }
    if request.user.username:
        user = User.objects.get(username=request.user.username)
        userinfo = UserInfo(user)
        basket = BasketDict(user)
        Uinfo = {
            "basket": len(basket[0]),
            "sum": basket[1],
            "user": user,
            "userinfo": userinfo
            }
        context.update(Uinfo)
    return render(request, 'Shop/index.html', context=context)


def order(request):
    user = User.objects.get(username=request.user.username)
    basket2 = BufBasket.objects.filter(user=user)
    listorder = []
    sum = 0
    for b in basket2:  # Добавляємо товари до замовлення
        product = Products.objects.get(id=b.prod.id)
        print(product.id)
        all = b.quantity * product.price
        sum += all

        listorder.append([product.name, b.quantity, float(product.price), float(all), product.id])

    descr = json.dumps(listorder)
    order1 = ListOrders(user=user, description=descr, status=1, date=timezone.now(), price=sum)
    order1.save()

    for prod in basket2:  # видаляємо записи з корзини
        prod.delete()

    # read = ListOrders.objects.get(user=user)
    # data = json.loads(read.description)

    return redirect('user')


def creat(request):
    category = Category.objects.all()
    if request.method == "POST":
        print("ЄЄЄЄ")
        prod = ProductsForm(request.POST, request.FILES)
        if prod.is_valid():
            produc = prod.save(commit=False)
            produc.published_date = timezone.now()
            produc.save()
            for img in request.FILES.getlist('img'):
                imgpost = ImgProduct(product=produc, img=img)
                imgpost.save()
            return index(request)
    else:
        context = {
            'category': category,
        }
        return render(request, 'Shop/creat.html', context=context)


def orders(request, id=None):
    orders = ListOrder()
    lnew = orders['lnew']
    lwork = orders['lwork']
    lend = orders['lend']
    buf_list = None
    if id == 1:
        buf_list = orders['new']
    elif id == 2:
        buf_list = orders['work']
    elif id == 3:
        buf_list = orders['end']
    print(buf_list)
    list_orders = list_orders = UpdateOrder(buf_list) # Перетворений список
    context = {
        'lnew': lnew,
        'lwork': lwork,
        'lend': lend,
        'list_orders': list_orders,
    }
    return render(request, 'Shop/orders.html', context=context)