import requests
import json
from config import OVERPASS_URL

query = """
    [out:json][timeout:60];
    area[name="Greater London"]->.searchArea;
    (   
        node["shop"](area.searchArea);
        way["shop"](area.searchArea);
        relation["shop"](area.searchArea);
    
        node["tourism"="artwork"](area.searchArea);
        way["tourism"="artwork"](area.searchArea);
        relation["tourism"="artwork"](area.searchArea);
    
        node["historic"="monument"](area.searchArea);
        way["historic"="monument"](area.searchArea);
        relation["historic"="monument"](area.searchArea);
    
        node["man_made"="statue"](area.searchArea);
        way["man_made"="statue"](area.searchArea);
        relation["man_made"="statue"](area.searchArea);
    );
    out center;
"""

response = requests.post(OVERPASS_URL, data={"data": query})
data = response.json()

if response.status_code != 200:
    print("!!! ERROR !!!")
    print(response.text)

print(data)
with open("overpass_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)