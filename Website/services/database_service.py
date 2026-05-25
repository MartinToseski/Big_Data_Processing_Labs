import sqlite3

DATABASE = 'database/website.db'


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ------------------------------------------------
# Cities
# ------------------------------------------------
def get_cities():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT DISTINCT city
    FROM places
    ORDER BY city
    ''')

    results = cursor.fetchall()
    conn.close()

    return results


# ------------------------------------------------
# Places By City
# ------------------------------------------------
def get_places_by_city(city):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT
        p.*,
        i.image_path
    FROM places p
    LEFT JOIN images i
    ON p.id = i.place_id
    WHERE p.city=?
    ORDER BY p.pagerank_score DESC
    ''', (city,))

    results = cursor.fetchall()
    conn.close()
    return results


# ------------------------------------------------
# Single Place
# ------------------------------------------------
def get_place(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT *
    FROM places
    WHERE id=?
    ''', (place_id,))

    result = cursor.fetchone()
    conn.close()

    return result


# ------------------------------------------------
# Place Image
# ------------------------------------------------
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