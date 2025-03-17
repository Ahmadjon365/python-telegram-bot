from geopy.geocoders import Nominatim

def get_location(latitude, longitude):
    geolocator = Nominatim(user_agent="name")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    return location.address

print(get_location(41.311081, 69.240562))
