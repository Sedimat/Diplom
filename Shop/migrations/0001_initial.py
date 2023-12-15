# Generated by Django 5.0 on 2023-12-15 14:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateTimeField(auto_created=True, verbose_name='Час')),
                ('name', models.CharField(max_length=20, verbose_name='Назва')),
                ('description', models.TextField(verbose_name='Опис')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Кількість')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ціна товару')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
            },
        ),
        migrations.CreateModel(
            name='ImgProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='prod.jpg', upload_to='img_product')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.products', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Зображення',
                'verbose_name_plural': 'Зображення',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='avatar.jpg', upload_to='avatar')),
                ('phone', models.CharField(max_length=13, verbose_name='Телефон')),
                ('address', models.TextField(verbose_name='Адреса')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Користувач',
                'verbose_name_plural': 'Користувачі',
            },
        ),
    ]
