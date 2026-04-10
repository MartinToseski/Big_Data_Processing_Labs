import requests
import json
from src.config import OVERPASS_URL


# Collect Raw Data
def fetch_osm_data(city, timeout=60):
    query = f"""
    [out:json][timeout:{timeout}];
    area[name="{city}"]->.searchArea;
    (
        node["shop"](area.searchArea);
    );
    out center;
    """

    response = requests.post(OVERPASS_URL, data={"data": query})

    if response.status_code != 200:
        raise Exception(f"Overpass API error: {response.text}")

    return response.json()


# Validate Data
def is_valid(element):
    tags = element.get("tags", {})

    if not element.get("id"):
        return False

    if not tags.get("name") and not tags.get("brand"):
        return False

    if not element.get("lat") and not element.get("lon") and not element.get("center"):
        return False

    if "shop" not in tags and "amenity" not in tags:
        return False

    return True


# Extract Features
def extract_core_features(element, city):
    tags = element.get("tags", {})

    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")

    name = tags.get("name") or tags.get("brand") or "unknown"

    return {
        "id": element.get("id"),
        "name": name,
        "city": city,
        "lat": lat,
        "lon": lon,
        "shop": tags.get("shop"),
        "amenity": tags.get("amenity"),
        "brand": tags.get("brand"),
        "wikidata": tags.get("brand:wikidata"),
        "wikipedia": tags.get("brand:wikipedia"),
        "street": tags.get("addr:street"),
        "house_number": tags.get("addr:housenumber"),
        "postcode": tags.get("addr:postcode"),
        "opening_hours": tags.get("opening_hours"),
    }


# Rule for Enrichment
def can_enrich(element):
    tags = element.get("raw_tags", {})

    if tags.get("brand:wikidata"):
        return True

    if tags.get("shop") in ["supermarket", "department_store", "convenience"]:
        return True

    if tags.get("amenity") in ["pharmacy", "bank", "restaurant"]:
        return True

    return False


# 5. OPTIONAL ENRICHMENT HOOK
def enrich_place(element):
    tags = element.get("raw_tags", {})

    element["is_chain"] = 1 if tags.get("brand") else 0
    element["has_wikidata"] = 1 if tags.get("brand:wikidata") else 0

    return element


# =========================
# 6. FULL PIPELINE
# =========================

def process_city(city):
    raw = fetch_osm_data(city)

    results = []
    rejected = 0

    for element in raw.get("elements", []):
        if not is_valid(element):
            rejected += 1
            continue

        place = extract_core_features(element, city)
        if can_enrich(place):
            place = enrich_place(place)
        results.append(place)

    print(f"[{city}] total={len(raw['elements'])}, kept={len(results)}, rejected={rejected}")
    return results


# Save Raw Data
def save_raw(data, path: str = "../../overpass_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Pipeline
if __name__ == "__main__":
    city = "Greater London"

    raw_data = fetch_osm_data(city)
    save_raw(raw_data)
    cleaned = process_city(city)

    print(f"Final dataset size: {len(cleaned)}")
    print(cleaned[:2])