import json
from init_db import connect
from src.collectors.wiki import enrich
from src.utils.city_centers import get_city_center


def distance(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2) ** 0.5


def encode_category(tags):
    if "historic" in tags or tags.get("tourism") == "artwork":
        return 1  # monuments/statues
    elif "shop" in tags:
        return 2  # shops
    return 0


def process(osm_data, raw_id, city):
    conn = connect()
    c = conn.cursor()

    center = get_city_center(city)

    if not center:
        print(f"Could not get center for {city}")
        return

    center_lat, center_lon = center

    count = 0

    for el in osm_data.get("elements", []):
        tags = el.get("tags", {})

        name = tags.get("name")
        lat = el.get("lat")
        lon = el.get("lon")

        # Skip invalid entries
        if not name or lat is None or lon is None:
            continue

        category = (
            tags.get("historic")
            or tags.get("tourism")
            or tags.get("shop")
            or "unknown"
        )

        wikidata_id, desc_len = enrich(tags)

        # -------- INTERMEDIATE --------
        c.execute("""
        INSERT INTO intermediate_data (
            raw_data_id, name, city, lat, lon,
            category, tags_json, wikidata_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            raw_id,
            name,
            city,
            lat,
            lon,
            category,
            json.dumps(tags),
            wikidata_id
        ))

        inter_id = c.lastrowid

        # -------- FEATURES --------
        dist = distance(lat, lon, center_lat, center_lon)
        tags_count = len(tags)

        has_website = 1 if "website" in tags else 0
        has_phone = 1 if "phone" in tags else 0

        is_tourism = 1 if (
            "historic" in tags or tags.get("tourism") == "artwork"
        ) else 0

        has_wiki = 1 if wikidata_id else 0

        category_encoded = encode_category(tags)

        c.execute("""
        INSERT INTO features (
            intermediate_id, name, city, lat, lon,
            distance_to_center, category_encoded,
            tags_count, description_length,
            has_website, has_wikipedia,
            is_tourism_place, has_phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            inter_id,
            name,
            city,
            lat,
            lon,
            dist,
            category_encoded,
            tags_count,
            desc_len,
            has_website,
            has_wiki,
            is_tourism,
            has_phone
        ))

        count += 1

    conn.commit()
    conn.close()

    print(f"{city}: processed {count} places")