import sqlite3


DATABASE_PATH = "../../database/image_database.db"


# -----------------------------------
# Create Database
# -----------------------------------
def create_database():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        image_path TEXT,
        image_class TEXT,
        palette_path TEXT,
        feature_vector TEXT
    )
    """

    cursor.execute(create_table_query)
    connection.commit()
    connection.close()


# -----------------------------------
# Insert Image Data
# -----------------------------------
def insert_image_data(image_name, image_path, image_class, palette_path, feature_vector):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    feature_vector_string = ""

    for i in range(len(feature_vector)):
        value = str(feature_vector[i])
        feature_vector_string = feature_vector_string + value

        if i != len(feature_vector) - 1:
            feature_vector_string = feature_vector_string + ","

    insert_query = """
    INSERT INTO images (
        image_name,
        image_path,
        image_class,
        palette_path,
        feature_vector
    )
    VALUES (?, ?, ?, ?, ?)
    """

    values = (image_name, image_path, image_class, palette_path, feature_vector_string)
    cursor.execute(insert_query, values)
    connection.commit()
    connection.close()


# -----------------------------------
# Load Entire Dataset
# -----------------------------------
def load_dataset():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    select_query = """
    SELECT
        image_name,
        image_path,
        image_class,
        palette_path,
        feature_vector
    FROM images
    """

    cursor.execute(select_query)
    rows = cursor.fetchall()
    connection.close()
    dataset = []

    for row in rows:
        image_name = row[0]
        image_path = row[1]
        image_class = row[2]
        palette_path = row[3]
        feature_vector_string = row[4]

        split_values = feature_vector_string.split(",")
        feature_vector = []

        for value in split_values:
            feature_vector.append(float(value))

        item = {
            "image_name": image_name,
            "image_path": image_path,
            "image_class": image_class,
            "palette_path": palette_path,
            "feature_vector": feature_vector
        }

        dataset.append(item)

    return dataset


# -----------------------------------
# Prevent Duplicate Processing
# -----------------------------------
def image_exists(image_path):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    query = """
    SELECT COUNT(*)
    FROM images
    WHERE image_path=?
    """

    cursor.execute(query, (image_path,))
    result = cursor.fetchone()
    connection.close()
    count = result[0]

    if count > 0:
        return True

    return False