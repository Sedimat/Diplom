from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:id>', views.page, name='page'),
    path('user', views.user, name='user'),
    path('order', views.order, name='order'),
    path('orders/<int:id>', views.orders, name='orders'),
    path('creat', views.creat, name='creat'),
    path("product/<int:id>", views.product, name="product"),
    path("status/<int:id>/<int:stat>", views.status, name="status"),
    path("edit_profile/<int:id>/<int:type>", views.edit_profile, name="edit_profile"),
    path("basket_del/<int:id>", views.basket_del, name="basket_del"),
    path("category/<str:name>/<int:id>", views.category, name="category"),
    path("login", LoginView.as_view(), name='login'),
    path("logout", views.logout_view, name='logout'),
    path("sessio/<int:id>", views.sessio, name='sessio'),
    path("basket", views.basket, name='basket'),
    path("no_user_basket_del/<int:id>", views.no_user_basket_del, name="no_user_basket_del"),
]

