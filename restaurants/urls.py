from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views


def custom_logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.signup_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/', views.search_restaurant, name='restaurant-search'),
    path('logout/', custom_logout_view, name='logout'),  # Use custom logout view
    path('restaurant/<str:restaurant_name>/', views.restaurant_details_view, name='restaurant_details'),  # New URL pattern
]
