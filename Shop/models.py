from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="Назва")
    img_cat = models.ImageField(upload_to='img_category', default='img_category/category.jpg')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Products(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Час")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна товару")  # вказує число флоат до коми та після
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категорія")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class ImgProduct(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товар")
    img = models.ImageField(upload_to='img_product', default='prod.jpg')

    def __str__(self):
        return f'Зображення товарів'

    class Meta:
        verbose_name = "Зображення товарів"
        verbose_name_plural = "Зображення товарів"


class UserProfile(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    avatar = models.ImageField(upload_to='avatar', default='avatar/avatar_crj2ayQ.jpg')
    phone = models.CharField(max_length=13, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адреса")

    def __str__(self):
        return f'Додаткова інформація'

    class Meta:
        verbose_name = "Користувач додаток"
        verbose_name_plural = "Користувачі додаток"

class BufBasket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    prod = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товари")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.user} - {self.prod} - {self.quantity}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

class ListOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    description = models.TextField(verbose_name="Замовлення")
    status = models.PositiveIntegerField(default=1, verbose_name="Статус")
    date = models.DateTimeField(auto_created=True, verbose_name="Час")
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1, verbose_name="Ціна замовлення")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

class Coments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупець")
    prod = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Товари")
    description = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Час")

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Коментарі"
        verbose_name_plural = "Коментарі"



# Create your models here.
