import os

from process_image import process_single_image
from palette_visualization import save_palette_image
from database_manager import create_database, insert_image_data, image_exists


RAW_DATA_FOLDER = "raw_data"
PALETTES_FOLDER = "palettes"
K_COLORS = 10


# -----------------------------------
# Create Database
# -----------------------------------
create_database()


# -----------------------------------
# Process Dataset
# -----------------------------------
for image_class in os.listdir(RAW_DATA_FOLDER):
    image_class_path = os.path.join(RAW_DATA_FOLDER, image_class)

    if os.path.isdir(image_class_path):
        for file_name in os.listdir(image_class_path):
            lower_name = file_name.lower()
            valid_image = False

            if lower_name.endswith(".jpg"):
                valid_image = True

            if lower_name.endswith(".jpeg"):
                valid_image = True

            if lower_name.endswith(".png"):
                valid_image = True

            if valid_image:
                image_path = os.path.join(image_class_path, file_name)
                already_processed = image_exists(image_path)

                if already_processed:
                    print()
                    print("Skipping:")
                    print(image_path)
                    continue

                print()
                print("Processing:")
                print(image_path)

                # -----------------------------------
                # Process Image
                # -----------------------------------
                sorted_centroids, feature_vector = process_single_image(image_path, k=K_COLORS)

                # -----------------------------------
                # Create Palette Path
                # -----------------------------------
                palette_image_class = os.path.join(PALETTES_FOLDER, image_class)

                if os.path.exists(palette_image_class) is False:
                    os.makedirs(palette_image_class)

                file_name_without_extension = os.path.splitext(file_name)[0]
                palette_file_name = file_name_without_extension + "_palette.png"
                palette_path = os.path.join(palette_image_class, palette_file_name)

                # -----------------------------------
                # Save Palette Image
                # -----------------------------------
                save_palette_image(sorted_centroids, palette_path)

                print("Saved palette:")
                print(palette_path)

                # -----------------------------------
                # Insert Into Database
                # -----------------------------------
                insert_image_data(
                    image_name=file_name,
                    image_path=image_path,
                    image_class=image_class,
                    palette_path=palette_path,
                    feature_vector=feature_vector
                )


print()
print("Database build completed.")