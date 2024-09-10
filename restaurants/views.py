# restaurants/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
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
    # get users location 
    user_lat = request.GET.get('lat', None)
    user_lng = request.GET.get('lng', None)

    #if location permissions not allowed
    if not user_lat or not user_lng:
        return render(request, 'restaurants/restaurant_list.html', {'error': 'User location not provided.'})
    
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    try:
        places_result = gmaps.places_nearby(
            location=(user_lat, user_lng),
            radius=3000,  # 3 km radius for nearby places
            type='restaurant'
        )

        # details of the top 3 closest restaurants
        closest_restaurants = []
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

    # render with the closest restaurants data
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': closest_restaurants})

def home(request):
    return render(request, 'restaurants/home.html')