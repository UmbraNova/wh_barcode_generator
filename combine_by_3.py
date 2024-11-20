import os
from PIL import Image


def combine_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    
    if len(png_files) < 3:  # Ensure there are at least 3 images to combine
        print("Not enough images to combine (minimum 3 needed).")
        return

    for i in range(0, len(png_files), 3):  # Process images in chunks of 3
        images_to_combine = png_files[i:i+3]  # Get the current batch of images
        
        images = [Image.open(os.path.join(input_folder, img)) for img in images_to_combine]
        max_width = max(img.width for img in images)  # Find the total width and total height
        total_height = sum(img.height for img in images)
        combined_image = Image.new('RGBA', (max_width, total_height))  # Create a new image to hold the combination
        
        # Stack the 3 images vertically
        y_offset = 0
        for img in images:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.height

        combined_image_name = f"combined_{i//3 + 1}.png"
        combined_image.save(os.path.join(output_folder, combined_image_name))
        print(f"Saved {combined_image_name}.")


input_folder = "X:/DEV/wh_barcode_generator/barcodes"
output_folder = "X:/DEV/wh_barcode_generator/barcodes_3"

combine_images(input_folder, output_folder)
