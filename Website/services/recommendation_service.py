from services.database_service import get_connection


# ------------------------------------------------
# Structural Recommendations
# ------------------------------------------------
def get_structural_recommendations(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT p.*
    FROM structural_recommendations sr
    JOIN places p
    ON sr.recommended_place_id = p.id
    WHERE sr.source_place_id=?
    ORDER BY sr.similarity_score DESC
    LIMIT 5
    ''', (place_id,))

    results = cursor.fetchall()
    conn.close()

    return results


# ------------------------------------------------
# Image Recommendations
# ------------------------------------------------
def get_image_recommendations(place_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT p.*
    FROM image_recommendations ir
    JOIN places p
    ON ir.recommended_place_id = p.id
    WHERE ir.source_place_id=?
    ORDER BY ir.similarity_score DESC
    LIMIT 5
    ''', (place_id,))

    results = cursor.fetchall()
    conn.close()

    return results