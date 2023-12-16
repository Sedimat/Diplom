from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.user, name='user'),
    path("product/<int:id>", views.product, name="product"),
    path("category/<str:name>", views.category, name="category"),
    path("login", LoginView.as_view(), name='login'),
    path("logout", views.logout_view, name='logout'),
]