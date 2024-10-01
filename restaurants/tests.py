import requests


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
        'key': "AIzaSyCqc613-d11926rxvX6oXwU2wYp3baIuP8"
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
        'fields': 'name,formatted_address,rating,formatted_phone_number,opening_hours,website,photos,price_level,reviews,business_status,url,types,user_ratings_total,geometry',
        'key': "AIzaSyCqc613-d11926rxvX6oXwU2wYp3baIuP8"
    }

    details_response = requests.get(DETAILS_API_URL, params=details_params)
    details_data = details_response.json()

    if 'result' not in details_data:
        return None, "Failed to retrieve details for this restaurant."

    restaurant = details_data['result']

    # Extract multiple photo URLs (up to 5) with higher resolution
    photos = []
    if restaurant.get('photos'):
        for photo in restaurant['photos'][:5]:  # Limit to 5 photos
            photo_reference = photo['photo_reference']
            # Increase maxwidth for better image quality (max is 1600)
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={photo_reference}&key=AIzaSyCqc613-d11926rxvX6oXwU2wYp3baIuP8"
            photos.append(photo_url)

    # Extract reviews (if available)
    reviews = []
    if restaurant.get('reviews'):
        for review in restaurant['reviews']:
            reviews.append({
                'author_name': review.get('author_name'),
                'rating': review.get('rating'),
                'text': review.get('text'),
                'time': review.get('relative_time_description')  # This often includes how long ago the review was posted
            })

    print(reviews)
    return restaurant, photos, reviews, None


get_restaurant_details("Blue India")