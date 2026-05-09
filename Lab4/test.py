import os
from process_image import process_single_image
from palette_visualization import save_palette_image

if __name__ == "__main__":
    image_path = "raw_data/sunset/sunset_1.jpg"
    sorted_centroids, feature_vector = process_single_image(image_path)

    relative_folder = os.path.dirname(image_path)
    relative_folder = relative_folder.replace("raw_data","palettes")

    os.makedirs(relative_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    palette_path = os.path.join(relative_folder, base_name + "_palette.png")
    save_palette_image(sorted_centroids, palette_path)