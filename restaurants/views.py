# restaurants/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import JsonResponse
import googlemaps
import requests


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
        
        return JsonResponse({'restaurants': closest_restaurants})
        
    # render with the closest restaurants data
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': closest_restaurants})

def home(request):
    return render(request, 'restaurants/home.html')

# Search for a restaurant 

# Google Places API endpoint
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"
TEXT_SEARCH_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


def get_restaurant_details(restaurant_name):
    if not restaurant_name:
        return None, "No restaurant name provided."

    # Step 1: Search for the restaurant using the 'find place from text' endpoint
    params = {
        'input': restaurant_name,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': settings.GOOGLE_MAPS_API_KEY
    }

    response = requests.get(PLACES_API_URL, params=params)
    data = response.json()

    if not data.get('candidates'):
        return None, "No results found for this restaurant."

    place_id = data['candidates'][0].get('place_id')
    if not place_id:
        return None, "Failed to retrieve the place ID for the restaurant."

    # Step 3: Fetch details using the place_id
    details_params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,rating,formatted_phone_number,opening_hours,website,photos,price_level,reviews,business_status,url,types,user_ratings_total',
        'key': settings.GOOGLE_MAPS_API_KEY
    }

    details_response = requests.get(DETAILS_API_URL, params=details_params)
    details_data = details_response.json()

    if 'result' not in details_data:
        return None, "Failed to retrieve details for this restaurant."

    restaurant = details_data['result']

    # Extract multiple photo URLs (up to 5 for example)
    photos = []
    if restaurant.get('photos'):
        for photo in restaurant['photos'][:5]:  # Limit to 5 photos
            photo_reference = photo['photo_reference']
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={settings.GOOGLE_MAPS_API_KEY}"
            photos.append(photo_url)

    return restaurant, photos, None


def get_restaurants_by_cuisine(cuisine, location="33.7490,-84.3880", radius=5000):
    """
    This function searches for restaurants that serve the given cuisine.
    :param cuisine: The type of cuisine (e.g., "Italian", "Mexican")
    :param location: Location coordinates (default: Atlanta, GA)
    :param radius: Search radius in meters (default: 5000 meters, ~3 miles)
    :return: List of restaurants or an error message.
    """
    params = {
        'query': f"{cuisine} restaurants",
        'location': location,
        'radius': radius,
        'type': 'restaurant',
        'key': settings.GOOGLE_MAPS_API_KEY
    }

    # Send a request to the Google Places Text Search API
    response = requests.get(TEXT_SEARCH_API_URL, params=params)
    data = response.json()

    if data.get('status') != "OK":
        return None, f"Error: {data.get('status')}"

    restaurants = data.get('results', [])
    # Limit the results to 10 restaurants
    return restaurants[:10], None


def search_restaurant(request):
    if request.method == "POST":
        # Check if we're searching by restaurant name
        restaurant_name = request.POST.get('restaurant_name')
        if restaurant_name:
            # Search by restaurant name
            restaurant_details, photos, error = get_restaurant_details(restaurant_name)

            if error:
                return render(request, 'restaurants/restaurant.html', {'error': error})

            context = {
                'restaurant': restaurant_details,
                'photos': photos
            }
            return render(request, 'restaurants/restaurant.html', context)

        # Check if we're searching by cuisine
        cuisine_type = request.POST.get('cuisine_type')
        near_me = request.POST.get('near_me')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # If "Near Me" is checked, use current location
        if near_me and latitude and longitude:
            location = f"{latitude},{longitude}"
            restaurants, error = get_restaurants_by_cuisine(cuisine_type, location=location)

            if error:
                return render(request, 'restaurants/restaurant.html', {'error': error})

            context = {
                'cuisine_restaurants': restaurants,
                'cuisine_type': cuisine_type
            }
            return render(request, 'restaurants/restaurant.html', context)

        # Otherwise, search by cuisine without location
        elif cuisine_type:
            restaurants, error = get_restaurants_by_cuisine(cuisine_type)

            if error:
                return render(request, 'restaurants/restaurant.html', {'error': error})

            context = {
                'cuisine_restaurants': restaurants,
                'cuisine_type': cuisine_type
            }
            return render(request, 'restaurants/restaurant.html', context)

    return render(request, 'restaurants/restaurant.html')
