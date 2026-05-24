from services.database_service import get_connection


def get_structural_recommendations(place_id):
    conn = get_connection()

    recommendations = conn.execute(
        '''
        SELECT *
        FROM places
        WHERE id != ?
        LIMIT 5
        ''',
        (place_id,)
    ).fetchall()

    conn.close()

    return recommendations



def get_same_city_image_recommendations(place_id):
    conn = get_connection()

    recommendations = conn.execute(
        '''
        SELECT *
        FROM places
        WHERE id != ?
        LIMIT 5
        ''',
        (place_id,)
    ).fetchall()

    conn.close()

    return recommendations



def get_other_city_image_recommendations(place_id):
    conn = get_connection()

    recommendations = conn.execute(
        '''
        SELECT *
        FROM places
        WHERE id != ?
        LIMIT 5
        ''',
        (place_id,)
    ).fetchall()

    conn.close()

    return recommendations