from database.database import get_connection

def get_cities():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
     SELECT *
     FROM cities
     ORDER BY name
     ''')

    results = cursor.fetchall()
    conn.close()
    return results


def get_places_by_city(city_id, sort="score"):
    conn = get_connection()
    cursor = conn.cursor()

    if sort == 'alphabetical':
        ordering = '''ORDER BY name ASC'''
    else:
        ordering = '''ORDER BY pagerank_score DESC'''

    query = f'''
        SELECT
            p.*,
            i.image_path
        FROM places p
        LEFT JOIN images i
        ON p.place_id = i.place_id
        WHERE p.city_id=?
        {ordering}
        '''

    cursor.execute(query, (city_id,))

    results = cursor.fetchall()
    conn.close()
    return results


def get_place(place_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
     SELECT
        p.*,
        c.name as city_name
     FROM places p
     JOIN cities c
     ON p.city_id = c.city_id
     WHERE p.place_id=?
     ''', (place_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def get_place_image(place_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
     SELECT *
     FROM images
     WHERE place_id=?
     LIMIT 1
     ''', (place_id,))

    result = cursor.fetchone()
    conn.close()
    return result


def get_city(city_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT *
    FROM cities
    WHERE city_id=?
    ''', (city_id,))

    result = cursor.fetchone()
    conn.close()
    return result