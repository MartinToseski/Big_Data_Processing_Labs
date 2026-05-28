from database.database import get_connection


def get_recommendations(place_id, recommendation_type, same_city=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
     SELECT
        p.*,
        c.name as city_name,
        i.image_path,
        i.palette_path,
        sp.similarity_score
     FROM similar_places sp
     JOIN places p
     ON sp.target_place_id = p.place_id
     JOIN cities c
     ON p.city_id = c.city_id
     LEFT JOIN images i
     ON p.place_id = i.place_id
     WHERE sp.source_place_id=?
     AND sp.recommendation_type=?
     '''

    params = [
        place_id,
        recommendation_type
    ]

    if same_city is not None:
        cursor.execute('''
         SELECT city_id
         FROM places
         WHERE place_id=?
         ''', (place_id,))

        city_id = cursor.fetchone()['city_id']

        if same_city:
            query += ' AND p.city_id=?'
        else:
            query += ' AND p.city_id!=?'
        params.append(city_id)

    query += ' LIMIT 5'
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
