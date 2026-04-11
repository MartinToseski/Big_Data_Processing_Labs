# Cities:
# - London
# - New York
# - Mexico City
# - Own Selected City (Berlin)
# Objects: Monuments/Statues & Shops/stores

DB_NAME = "lab2.db"

CITIES = [
    "London",
    "New York",
    "Mexico City",
    "Berlin"
]

PLACE_TYPES = [
    "monument",
    "statue",
    "shop",
    "store"
]

MIN_OBJECTS_PER_CITY = 200
REQUEST_DELAY = 0.5
MAX_RETRIES = 5

OVERPASS_API = "https://overpass-api.de/api/interpreter"
WIKI_API = "https://en.wikipedia.org/w/api.php"
NOMINATIM_API = "https://nominatim.openstreetmap.org/search"