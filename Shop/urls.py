from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:id>', views.page, name='page'),
    path('user', views.user, name='user'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('order', views.order, name='order'),
    path('orders/<int:id>', views.orders, name='orders'),
    path('orders0/<int:id>', views.orders0, name='orders0'),
    path('creat', views.creat, name='creat'),
    path("product/<int:id>", views.product, name="product"),
    path("status/<int:id>/<int:stat>", views.status, name="status"),
    path("status0/<int:id>/<int:stat>", views.status0, name="status0"),
    path("edit_profile/<int:id>/<int:type>", views.edit_profile, name="edit_profile"),
    path("basket_del/<int:id>", views.basket_del, name="basket_del"),
    path("category/<str:name>/<int:id>", views.category, name="category"),
    path("login", LoginView.as_view(), name='login'),
    path("logout", views.logout_view, name='logout'),
    path("sessio/<int:id>", views.sessio, name='sessio'),
    path("basket", views.basket, name='basket'),
    path("no_user_basket_del/<int:id>", views.no_user_basket_del, name="no_user_basket_del"),
    path("no_user_orders", views.no_user_orders, name="no_user_orders"),
    path("address/<int:id>", views.address, name="address"),
]

