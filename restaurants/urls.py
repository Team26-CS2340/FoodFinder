# restaurants/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('about/', views.about, name='about'),
    path('favorites/', views.favorites, name='favorites')
]
