# Cities:
# - London
# - New York
# - Mexico City
# - Own Selected City (Berlin)
# Objects: Monuments/Statues & Shops/stores

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "lab2.db")

CITIES = [
    "London",
    "New York",
    "Ciudad de México",
    "Berlin"
]

PLACE_TYPES = [
    "monument",
    "statue",
    "shop",
    "store"
]

HEADERS = {
    "User-Agent": "big-data-lab-project"
}

MIN_OBJECTS_PER_CITY = 200
REQUEST_DELAY = 0.5
MAX_RETRIES = 5

OVERPASS_API = "https://overpass-api.de/api/interpreter"
WIKI_API = "https://en.wikipedia.org/w/api.php"
NOMINATIM_API = "https://nominatim.openstreetmap.org/search"