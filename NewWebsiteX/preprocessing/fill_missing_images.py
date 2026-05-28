import sqlite3
import os
import requests
import urllib.parse
import time
import re

from PIL import Image
from io import BytesIO


DATABASE = "database/website.db"

HEADERS = {
    "User-Agent":
    "TourismRecommendationSystem"
}


def safe_json(url):
    for attempt in range(5):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )

            if response.status_code == 429:
                wait = 2**attempt
                print(f"Rate limited ({wait}s)")
                time.sleep(wait)
                continue

            return response.json()
        except:
            time.sleep(2**attempt)

    return None


def clean_filename(text):
    text = text.strip()
    text = text.replace(
        " ",
        "_"
    )
    text = re.sub(
        r'[\\/*?:"<>|]',
        '',
        text
    )
    return text


conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""
SELECT
    p.place_id,
    p.name,
    p.city_id,
    p.wiki_url,
    c.name AS city_name
FROM places p
JOIN cities c
ON p.city_id = c.city_id
WHERE p.has_image=0
""")

places = cursor.fetchall()
print("Missing images:", len(places))

for place in places:
    print(
        "\nTrying:",
        place["name"]
    )
    try:
        title = urllib.parse.unquote(
            place[
                "wiki_url"
            ].split("/")[-1]

        )

        api = (
            "https://en.wikipedia.org/w/api.php"
            "?action=query"
            "&prop=pageimages"
            "&piprop=thumbnail"
            "&pithumbsize=1200"
            "&titles="
            +
            urllib.parse.quote(title)
            +
            "&format=json"
        )

        data = safe_json(api)

        if not data:
            continue

        pages = data.get(
            "query",
            {}
        ).get(
            "pages",
            {}
        )

        image_url = None
        for page in pages.values():
            if "thumbnail" in page:
                image_url = page["thumbnail"]["source"]

        if not image_url:
            print("No thumbnail")
            continue

        response = requests.get(
            image_url,
            headers=HEADERS,
            timeout=20
        )

        content = response.headers.get(
            "content-type",
            ""
        ).lower()

        if "image" not in content:
            print(
                "Not image:",
                content
            )
            continue
        try:
            image = Image.open(
                BytesIO(
                    response.content
                )
            ).convert(
                "RGB"
            )
        except:
            print(
                "Invalid image"
            )
            continue


        city_folder = clean_filename(place["city_name"].lower())

        folder = os.path.join(
            "static",
            "images",
            city_folder
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        filename = (
            clean_filename(place["name"])
            +
            ".jpg"
        )

        save_path = os.path.join(
            folder,
            filename
        )

        image.save(
            save_path,
            quality=90
        )


        relative_path = os.path.join(
            "images",
            city_folder,
            filename
        ).replace(
            "\\",
            "/"
        )

        cursor.execute("""
        INSERT INTO images(
            place_id,
            image_path
        )
        VALUES(?,?)
        """,(
            place["place_id"],
            relative_path
        ))


        cursor.execute("""
        UPDATE places
        SET has_image=1
        WHERE place_id=?
        """,(place["place_id"],))

        conn.commit()

        print("Added")

    except Exception as error:
        print(error)

    time.sleep(0.7)


conn.close()
print("\nFinished.")