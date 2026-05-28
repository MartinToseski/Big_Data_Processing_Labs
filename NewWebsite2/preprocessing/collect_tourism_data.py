import requests
import sqlite3
import os
import time
import urllib.parse

from io import BytesIO
from PIL import Image

BASE_DIR = os.path.dirname(__file__)

DATABASE = os.path.join(
    BASE_DIR,
    '..',
    'database',
    'website.db'
)

cities = [
    'Berlin',
    'London',
    'New York',
    'Ciudad de México'
]

HEADERS = {
    'User-Agent': 'TourismRecommendationSystem/1.0'
}


def safe_json_request(
        url,
        retries=5,
        base_delay=1
):

    for attempt in range(retries):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )

            if response.status_code == 429:

                delay = base_delay * (2 ** attempt)

                print(
                    f'Rate limited. '
                    f'Waiting {delay}s...'
                )

                time.sleep(delay)

                continue

            if response.status_code != 200:

                delay = base_delay * (2 ** attempt)

                print(
                    f'HTTP {response.status_code}. '
                    f'Retrying in {delay}s...'
                )

                time.sleep(delay)

                continue

            try:
                return response.json()

            except:

                delay = base_delay * (2 ** attempt)

                print(
                    f'Invalid JSON. '
                    f'Retrying in {delay}s...'
                )

                time.sleep(delay)

        except Exception as error:

            delay = base_delay * (2 ** attempt)

            print(
                f'Request failed: {error}. '
                f'Retrying in {delay}s...'
            )

            time.sleep(delay)

    return None


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

os.makedirs('static/images', exist_ok=True)

bad_keywords = [
    'List of',
    'Tourism in',
    'tourism in',
    'Airport',
    'airport',
    'Economy',
    'economy',
    'Tourist attraction',
    'tourist attraction'
]

city_keywords = {
    'Berlin': ['berlin'],
    'London': ['london', 'england', 'westminster'],
    'New York': ['new york', 'manhattan'],
    'Ciudad de México': [
        'mexico city',
        'ciudad de méxico',
        'mexico'
    ]
}

for city in cities:

    print(f'\nCollecting data for {city}...\n')

    cursor.execute(
        'INSERT OR IGNORE INTO cities(name) VALUES(?)',
        (city,)
    )

    conn.commit()

    cursor.execute(
        'SELECT city_id FROM cities WHERE name=?',
        (city,)
    )

    city_id = cursor.fetchone()[0]

    search_query = urllib.parse.quote(
        f'tourist attractions in {city}'
    )

    search_url = (
        'https://en.wikipedia.org/w/api.php'
        '?action=query'
        '&list=search'
        '&format=json'
        '&srlimit=100'
        f'&srsearch={search_query}'
    )

    response = safe_json_request(search_url)

    if not response:
        continue

    pages = response['query']['search']

    for page in pages:

        try:

            title = page['title']

            if any(
                    keyword in title
                    for keyword in bad_keywords
            ):
                continue

            summary = page['snippet']

            keywords = city_keywords.get(
                city,
                [city.lower()]
            )

            combined_text = (
                title + ' ' + summary
            ).lower()

            encoded_title = urllib.parse.quote(title)

            lat = 0
            lon = 0

            wiki_url = (
                'https://en.wikipedia.org/wiki/' +
                title.replace(' ', '_')
            )

            # ----------------------------------------
            # LINKS
            # ----------------------------------------

            links_url = (
                'https://en.wikipedia.org/w/api.php'
                '?action=query'
                '&prop=links'
                '&pllimit=max'
                '&format=json'
                f'&titles={encoded_title}'
            )

            links_data = safe_json_request(
                links_url
            )

            wiki_links = []

            if links_data:

                for value in links_data['query']['pages'].values():

                    if 'links' not in value:
                        continue

                    for link in value['links']:

                        wiki_links.append(
                            link['title']
                        )

            wiki_links_text = '|'.join(
                wiki_links
            )

            # ----------------------------------------
            # COORDINATES
            # ----------------------------------------

            coord_url = (
                'https://en.wikipedia.org/w/api.php'
                '?action=query'
                '&prop=coordinates'
                '&format=json'
                f'&titles={encoded_title}'
            )

            coord_data = safe_json_request(
                coord_url
            )

            if coord_data:

                for value in coord_data['query']['pages'].values():

                    if 'coordinates' in value:

                        lat = value['coordinates'][0]['lat']
                        lon = value['coordinates'][0]['lon']

            # ----------------------------------------
            # GET MULTIPLE IMAGES
            # ----------------------------------------

            images_api = (
                'https://en.wikipedia.org/w/api.php'
                '?action=query'
                '&prop=images'
                '&imlimit=6'
                '&format=json'
                f'&titles={encoded_title}'
            )

            images_data = safe_json_request(
                images_api
            )

            candidate_images = []

            if images_data:

                for value in images_data['query']['pages'].values():

                    if 'images' not in value:
                        continue

                    for image in value['images']:

                        image_title = image['title']

                        candidate_images.append(
                            image_title
                        )

            local_image_path = ''

            for candidate in candidate_images:

                try:

                    image_info_api = (
                        'https://en.wikipedia.org/w/api.php'
                        '?action=query'
                        '&prop=imageinfo'
                        '&iiprop=url'
                        '&format=json'
                        f'&titles={urllib.parse.quote(candidate)}'
                    )

                    image_info = safe_json_request(
                        image_info_api
                    )

                    if not image_info:
                        continue

                    image_url = None

                    for value in image_info['query']['pages'].values():

                        if 'imageinfo' not in value:
                            continue

                        image_url = value['imageinfo'][0]['url']

                    if not image_url:
                        continue

                    extension = (
                        image_url.split('.')[-1]
                        .lower()
                        .split('?')[0]
                    )

                    valid_extensions = [
                        'jpg',
                        'jpeg',
                        'png',
                        'webp',
                        'jfif',
                        'JPG',
                        'JPEG',
                        'PNG',
                        'WEBP'
                    ]

                    if extension not in valid_extensions:
                        continue

                    success = False

                    for attempt in range(3):

                        try:

                            image_response = requests.get(
                                image_url,
                                headers=HEADERS,
                                timeout=20
                            )

                            if image_response.status_code == 200:
                                success = True
                                break

                        except:

                            pass

                        time.sleep(2 ** attempt)

                    if not success:
                        continue

                    image = Image.open(
                        BytesIO(
                            image_response.content
                        )
                    ).convert('RGB')

                    width, height = image.size

                    filename = (
                        title.replace('/', '_')
                        .replace(' ', '_')
                        .replace(':', '_')
                        .replace('?', '_')
                        + '.' + extension
                    )

                    local_folder = (
                        f'static/images/'
                        f'{city.lower().replace(" ", "_")}'
                    )

                    os.makedirs(
                        local_folder,
                        exist_ok=True
                    )

                    local_path = os.path.join(
                        local_folder,
                        filename
                    )

                    image.save(local_path)

                    local_image_path = (
                        f'images/'
                        f'{city.lower().replace(" ", "_")}/'
                        f'{filename}'
                    )

                    print(
                        f'Valid image selected: {title}'
                    )

                    break


                except Exception as error:

                    print(

                        f'Image failed {candidate}:',

                        error

                    )

                    continue

            # ----------------------------------------
            # INSERT PLACE
            # ----------------------------------------

            cursor.execute('''
            INSERT INTO places (
                city_id,
                name,
                description,
                lat,
                lon,
                wiki_url,
                wiki_summary,
                wiki_links,
                image_url,
                pagerank_score,
                relevance_score,
                has_image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                city_id,
                title,
                summary,
                lat,
                lon,
                wiki_url,
                summary,
                wiki_links_text,
                local_image_path,
                0,
                0,
                1 if local_image_path else 0
            ))

            place_id = cursor.lastrowid

            # ----------------------------------------
            # INSERT IMAGE
            # ----------------------------------------

            if local_image_path:

                cursor.execute('''
                INSERT INTO images (
                    place_id,
                    image_name,
                    image_path,
                    palette_path,
                    feature_vector,
                    image_class
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    place_id,
                    filename,
                    local_image_path,
                    '',
                    '',
                    'wiki'
                ))

            conn.commit()

            print(f'Collected: {title}')

            time.sleep(0.5)

        except Exception as error:

            print(
                f'Error processing {title}: '
                f'{error}'
            )

            continue

conn.close()

print('\nTourism data collection complete.')