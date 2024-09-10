import googlemaps

# Replace this with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyCqc613-d11926rxvX6oXwU2wYp3baIuP8'

def test_google_maps_api(lat, lng):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    try:
        # Make the places_nearby API call to get nearby restaurants
        places_result = gmaps.places_nearby(
            location=(lat, lng),
            # radius=3000,  # 3 km radius for nearby places <- rank_by='distance' is used instead bc its more accurate
            rank_by='distance',
            type='food|restaurant|establishment'
        )

        # Print the result for debugging
        print("API call successful. Results:")
        for place in places_result['results'][:10]:  # Print top 3 restaurants
            print(f"Name: {place.get('name')}")
            print(f"Rating: {place.get('rating')}")
            print(f"Address: {place.get('vicinity')}")
            print(f"Types: {place.get('types', [])}")
            print("-" * 40)

    except Exception as e:
        print(f"Error during API call: {str(e)}")


# Example coordinates (latitude, longitude)
lat = 33.777 
lng = -84.388

print(f"Testing Google Maps API with location: {lat}, {lng}")
test_google_maps_api(lat, lng)
