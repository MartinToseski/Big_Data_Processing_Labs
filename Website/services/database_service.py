import sqlite3

DB_PATH = 'database/website.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_cities():
    conn = get_connection()
    cities = conn.execute(
        'SELECT DISTINCT city FROM places'
    ).fetchall()
    conn.close()
    return cities


def get_places_by_city(city_name):
    conn = get_connection()
    places = conn.execute(
        '''
        SELECT *
        FROM places
        WHERE city = ?
        ORDER BY pagerank_score DESC
        ''',
        (city_name,)
    ).fetchall()
    conn.close()
    return places


def get_place_by_id(place_id):
    conn = get_connection()
    place = conn.execute(
        '''
        SELECT *
        FROM places
        WHERE id = ?
        ''',
        (place_id,)
    ).fetchone()
    conn.close()
    return place