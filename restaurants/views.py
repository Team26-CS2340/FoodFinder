# restaurants/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('restaurant_list')  # Redirect to homepage
    else:
        form = AuthenticationForm()

    return render(request, 'restaurants/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically log the user in after signup
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            login(request, user)
            return redirect('restaurant_list')  # Redirect to homepage
    else:
        form = UserRegistrationForm()

    return render(request, 'restaurants/register.html', {'form': form})


from django.shortcuts import render


def restaurant_list(request):
    # Random hardcoded restaurant data
    restaurants = [
        {
            'name': 'The Gourmet Spot',
            'cuisine': 'Italian',
            'rating': 4.5,
            'address': '123 Foodie Lane, Culinary City',
        },
        {
            'name': 'Sushi Delight',
            'cuisine': 'Japanese',
            'rating': 4.7,
            'address': '456 Ocean Avenue, Seafood Town',
        },
        {
            'name': 'BBQ Bonanza',
            'cuisine': 'American',
            'rating': 4.2,
            'address': '789 Grill Street, Smokeville',
        },
    ]

    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def home(request):
    return render(request, 'restaurants/home.html')