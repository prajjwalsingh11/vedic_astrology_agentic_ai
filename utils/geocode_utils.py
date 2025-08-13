try:
    from geopy.geocoders import Nominatim
except ImportError:
    Nominatim = None
    print("geopy not installed. Latitude/Longitude will use demo values.")


def get_lat_lon(city_name: str):
    if Nominatim is None or not city_name.strip():
        return 0.0, 0.0

    try:
        geolocator = Nominatim(user_agent="astroagent")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not find city '{city_name}', using demo coordinates.")
            return 0.0, 0.0
    except Exception as e:
        print(f"Error fetching coordinates for '{city_name}': {e}. Using demo values.")
        return 0.0, 0.0
