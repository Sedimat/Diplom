from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:id>', views.page, name='page'),
    path('user', views.user, name='user'),
    path('order', views.order, name='order'),
    path('creat', views.creat, name='creat'),
    path("product/<int:id>", views.product, name="product"),
    path("basket_del/<int:id>", views.basket_del, name="basket_del"),
    path("category/<str:name>/<int:id>", views.category, name="category"),
    path("login", LoginView.as_view(), name='login'),
    path("logout", views.logout_view, name='logout'),
]

