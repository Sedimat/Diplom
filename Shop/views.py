import json

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserRegistrationForm, UserProfileForm, BasketForm, ProductsForm, ImgProductForm, ComentsForm, \
    NoUserListOrdersForm
from .models import UserProfile, Products, ImgProduct, Category, BufBasket, ListOrders, Coments, NoUserListOrders


# Create your views here.

def NoUserOrder(request):
    sess = request.session.get('sess')
    if sess == None:
        return []
    len_order = []
    sum2 = 0
    prods = []
    lenProd = 0
    count = 0
    print(lenProd)
    for i in sess:
        price = 0
        product = Products.objects.get(id=i[1])
        imgs = ImgProduct.objects.filter(product=product.id)
        lenProd += i[0]
        price = product.price * i[0]
        sum2 += price
        prods.append([product.name, imgs[0], product.price, i[0], price, count])
        count += 1

    len_order = [prods, lenProd, sum2]
    return {'no_user': len_order}


def NoUserUpdateOrder(orders):
    no_user_list = []
    for i in orders:
        desc = json.loads(i.description)
        buf = []
        for a in desc:
            product = get_object_or_404(Products, id=a[1])
            imgs = ImgProduct.objects.filter(product=product.id)
            buf.append([product, imgs[0], a[2], a[3], a[0]])
        no_user_list.append([buf, i.name, i.phone, i.address, i.status, i.date, i.price, i.id])
    return {"no_user_list": no_user_list}


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
    new = ListOrders.objects.filter(status=1).order_by("-date")  # сортує по даті додавання
    work = ListOrders.objects.filter(status=2).order_by("-date")  # сортує по даті додавання
    end = ListOrders.objects.filter(status=3).order_by("-date")  # сортує по даті додавання
    return {'new': new, 'work': work, 'end': end, 'lnew': len(new), 'lwork': len(work), 'lend': len(end)}


def NoUserListOrder():
    new = NoUserListOrders.objects.filter(status=1).order_by("-date")  # сортує по даті додавання
    work = NoUserListOrders.objects.filter(status=2).order_by("-date")  # сортує по даті додавання
    end = NoUserListOrders.objects.filter(status=3).order_by("-date")  # сортує по даті додавання
    return {'NUnew': new, 'NUwork': work, 'NUend': end, 'NUlnew': len(new), 'NUlwork': len(work), 'NUlend': len(end)}


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
    return (basket, sum,)


def index(request):
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', None))
    user_agent = request.META.get('HTTP_USER_AGENT', '')  # додаткова інфа
    print(client_ip)
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
    else:
        context.update(NoUserOrder(request))

    return render(request, 'Shop/index.html', context=context)


def product(request, id=None):
    product = get_object_or_404(Products, id=id)
    coments = Coments.objects.filter(prod=product.id).order_by("-published_date")
    coms = []
    for i in coments:
        user_inf = UserProfile.objects.get(id_user=i.user)
        bufcoms = [i.user, i.prod, i.description, i.published_date, user_inf.avatar]
        coms.append(bufcoms)

    imgs = ImgProduct.objects.filter(product=product.id)
    category = Category.objects.all()
    if request.method == "POST":
        formC = ComentsForm(request.POST)
        if formC.is_valid():
            coment = formC.save(commit=False)
            coment.user = request.user
            coment.prod = product
            coment.published_date = timezone.now()
            coment.save()
            return redirect('product', id=id)

    if request.method == "POST":
        form = BasketForm(request.POST)
        if form.is_valid() and request.user:
            bask = form.save(commit=False)
            bask.user = request.user
            bask.prod = product
            bask.save()
            return redirect('product', id=id)

    context = {
        "coments": coms,
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
    else:
        context.update(NoUserOrder(request))

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
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            profile = UserProfile(id_user=user, avatar='avatar/avatar_crj2ayQ.jpg', phone=' ', address=' ')
            profile.save()
            return render(request, 'Shop/user.html', context={"a": "Ви успішно зареєструвались"})
        else:
            # Якщо форма не валідна, отримайте доступ до помилок
            errors = user_form.errors
            return render(request, 'Shop/user.html', context={"a": errors})

    if request.user.username:
        user = User.objects.get(username=request.user.username)
        orders = ListOrders.objects.filter(user=user).order_by("-date")
        list_orders = UpdateOrder(orders)  # Перетворений список
        basket_buf = BasketDict(user)

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
        context.update(NoUserListOrder())

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
    if len(basket2) > 0:
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

        return redirect('user')
    else:
        return redirect('user')


def creat(request):
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
    orders1 = NoUserListOrder()
    NUlnew = orders1['NUlnew']
    NUlwork = orders1['NUlwork']
    NUlend = orders1['NUlend']
    buf_list = None
    if id == 1:
        buf_list = orders['new']
    elif id == 2:
        buf_list = orders['work']
    elif id == 3:
        buf_list = orders['end']
    list_orders = UpdateOrder(buf_list)  # Перетворений список
    context = {
        'lnew': lnew,
        'lwork': lwork,
        'lend': lend,
        "NUlnew": NUlnew,
        "NUlwork": NUlwork,
        "NUlend": NUlend,
        'list_orders': list_orders,
    }
    return render(request, 'Shop/orders.html', context=context)


def status(request, id=None, stat=None):
    order = ListOrders.objects.get(id=id)
    order.status = stat
    order.save()
    return redirect('orders', id=stat)


def edit_profile(request, id=None, type=None):
    if type == 1:
        if request.method == "POST":
            if 'avatar' in request.FILES:
                avatar_file = request.FILES['avatar']
                user_prof = UserProfile.objects.get(id_user=id)
                user_prof.avatar = avatar_file
                user_prof.save()
    if type == 2:
        if request.method == "POST":
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            if phone not in [None, ''] and address not in [None, '']:
                user_prof = UserProfile.objects.get(id_user=id)
                user_prof.phone = phone
                user_prof.address = address
                user_prof.save()
    return redirect('user')


def sessio(request, id=None):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        # request.session.flush() # видаляєму все
        # del request.session['sess'] # видаляє тільки цю сесію
        buf = request.session.get('sess')
        if buf == None:
            buf = []
        if any(x[1] == id for x in buf):
            for i in buf:
                if i[1] == id:
                    i[0] += quantity
            request.session['sess'] = buf
        else:
            buf.append([quantity, id])
            request.session['sess'] = buf
        print(request.session.get('sess'))

    return redirect('product', id=id)


def basket(request):
    context = {}
    if request.user.username:
        return redirect('user')
    else:
        context.update(NoUserOrder(request))

    return render(request, 'Shop/basket.html', context=context)


def no_user_basket_del(request, id=None):
    sess = request.session.get('sess')
    sess.pop(id)
    return redirect('basket')


def no_user_orders(request):
    sess = request.session.get('sess')
    if request.method == "POST":
        order = NoUserListOrdersForm(request.POST)

        if order.is_valid():
            list_order = []
            all_price = 0
            for i in sess:
                prod = Products.objects.get(id=i[1])
                sum_price = i[0] * float(prod.price)
                all_price += sum_price
                list_order.append([i[0], i[1], float(prod.price), sum_price])

            u_order = order.save(commit=False)
            u_order.description = json.dumps(list_order)
            u_order.status = 1
            u_order.price = all_price
            u_order.date = timezone.now()
            u_order.save()
            del request.session['sess']  # видаляє тільки цю сесію
        else:
            error = order.errors
            context = {"error": error}
            context.update(NoUserOrder(request))

            return render(request, 'Shop/basket.html', context=context)

    return redirect('basket')


def orders0(request, id=None):
    orders = ListOrder()
    lnew = orders['lnew']
    lwork = orders['lwork']
    lend = orders['lend']
    orders = NoUserListOrder()
    NUlnew = orders['NUlnew']
    NUlwork = orders['NUlwork']
    NUlend = orders['NUlend']
    buf_list = None
    if id == 1:
        buf_list = orders['NUnew']
    elif id == 2:
        buf_list = orders['NUwork']
    elif id == 3:
        buf_list = orders['NUend']
    context = {
        'lnew': lnew,
        'lwork': lwork,
        'lend': lend,
        "NUlnew": NUlnew,
        "NUlwork": NUlwork,
        "NUlend": NUlend
    }
    context.update(NoUserUpdateOrder(buf_list))
    return render(request, 'Shop/orders0.html', context=context)


def status0(request, id=None, stat=None):
    order = NoUserListOrders.objects.get(id=id)
    order.status = stat
    order.save()
    return redirect('orders0', id=stat)
