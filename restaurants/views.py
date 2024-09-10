# restaurants/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import JsonResponse
import googlemaps


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
    closest_restaurants = []
    # get users location 
    if request.method == 'POST':
        user_lat = request.POST.get('lat', None)
        user_lng = request.POST.get('lng', None)

        #if location permissions not allowed
        if user_lat and user_lng:
            try:
                # initialize google maps client
                gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

                places_result = gmaps.places_nearby(
                    location=(float(user_lat), float(user_lng)),
                    # radius=3000,  # 3 km radius for nearby places <- rank_by='distance' is used instead bc its more accurate
                    rank_by='distance',
                    type='restaurant'
                )

                # details of the closest restaurants
                for place in places_result['results'][:3]:
                    restaurant = {
                        'name': place.get('name'),
                        'rating': place.get('rating'),
                        'address': place.get('vicinity'),
                        'cuisine': place.get('types', [])  # types isnt exactly cuisine so we prob need to delete
                    }
                    closest_restaurants.append(restaurant)
                
            except Exception as e:
                return render(request, 'restaurants/restaurant_list.html', {'error': str(e)})
        else:
            return render(request, 'restaurants/restaurant_list.html', {'error': 'Location not provided.'})
    # render with the closest restaurants data
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': closest_restaurants})

def home(request):
    return render(request, 'restaurants/home.html')