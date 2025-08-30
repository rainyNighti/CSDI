import os
import shutil
from PIL import Image
import random

from datasets.dataset_split import val_names  # List of validation image filenames to exclude


def apply_zoom_in(img, factor):
    """Helper function: Apply center zoom-in effect."""
    original_size = img.size
    new_width = int(original_size[0] / factor)
    new_height = int(original_size[1] / factor)
    left = (original_size[0] - new_width) // 2
    top = (original_size[1] - new_height) // 2
    cropped_img = img.crop((left, top, left + new_width, top + new_height))
    return cropped_img.resize(original_size, Image.Resampling.LANCZOS)


def apply_combo_transform(img, angle, zoom_factor):
    """
    Helper function: Apply combined transform (rotate then zoom).

    :param img: Input PIL Image object.
    :param angle: Rotation angle in degrees.
    :param zoom_factor: Zoom factor (e.g., 1.2 means 20% zoom-in).
    :return: Transformed PIL Image object.
    """
    original_size = img.size

    # Step 1: Rotate the image
    rotated_img = img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor='black')

    # Step 2: Center crop to achieve zoom effect
    new_width = int(original_size[0] / zoom_factor)
    new_height = int(original_size[1] / zoom_factor)
    left = (original_size[0] - new_width) // 2
    top = (original_size[1] - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    cropped_rotated_img = rotated_img.crop((left, top, right, bottom))

    # Step 3: Resize back to original dimensions
    final_img = cropped_rotated_img.resize(original_size, Image.Resampling.LANCZOS)
    return final_img


def process_images_ultimate(source_folder, output_folder, rotation_angle_range=15, zoom_in_range=(1.05, 1.17)):
    """
    Ultimate data augmentation script: all transforms use independent random parameters.
    - 2x independent random rotations
    - 2x independent random zooms
    - 2x independent random rotation + zoom combinations
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

    for filename in os.listdir(source_folder):
        if filename in val_names:  # Skip validation dataset
            continue

        if not filename.lower().endswith(supported_extensions):
            continue

        source_path = os.path.join(source_folder, filename)

        try:
            shutil.copy2(source_path, output_folder)
            print(f"Copied original: {filename}")
        except Exception as e:
            print(f"Error copying file {filename}: {e}")
            continue

        try:
            with Image.open(source_path) as img:
                name, ext = os.path.splitext(filename)

                # --- 1. Generate independent random parameters for all transforms ---
                standalone_rot_angle1 = random.uniform(5, rotation_angle_range)
                standalone_rot_angle2 = random.uniform(-rotation_angle_range, -5)

                standalone_zoom_factor1 = random.uniform(zoom_in_range[0], zoom_in_range[1])
                standalone_zoom_factor2 = random.uniform(zoom_in_range[0], zoom_in_range[1])

                combo_rot_angle1 = random.uniform(5, rotation_angle_range)
                combo_zoom_factor1 = random.uniform(zoom_in_range[0], zoom_in_range[1])
                combo_rot_angle2 = random.uniform(-rotation_angle_range, -5)
                combo_zoom_factor2 = random.uniform(zoom_in_range[0], zoom_in_range[1])

                # --- 2. Apply independent rotations (2 images) ---
                for i, angle in enumerate([standalone_rot_angle1, standalone_rot_angle2]):
                    rotated_img = img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor='black')
                    rotated_filename = f"{name}_rot_{i + 1}_{int(angle)}deg{ext}"
                    rotated_img.save(os.path.join(output_folder, rotated_filename))
                    print(f"  -> Created rotated image: {rotated_filename}")

                # --- 3. Apply independent zooms (2 images) ---
                for i, factor in enumerate([standalone_zoom_factor1, standalone_zoom_factor2]):
                    zoomed_img = apply_zoom_in(img, factor)
                    zoomed_filename = f"{name}_zoom_{i + 1}_{int(factor * 100)}pct{ext}"
                    zoomed_img.save(os.path.join(output_folder, zoomed_filename))
                    print(f"  -> Created zoomed image: {zoomed_filename}")

                # --- 4. Apply rotation+zoom combos (2 images) ---
                combo_img1 = apply_combo_transform(img, combo_rot_angle1, combo_zoom_factor1)
                combo_filename1 = f"{name}_combo_{int(combo_rot_angle1)}deg_{int(combo_zoom_factor1 * 100)}pct{ext}"
                combo_img1.save(os.path.join(output_folder, combo_filename1))
                print(f"  -> Created combo image: {combo_filename1}")

                combo_img2 = apply_combo_transform(img, combo_rot_angle2, combo_zoom_factor2)
                combo_filename2 = f"{name}_combo_{int(combo_rot_angle2)}deg_{int(combo_zoom_factor2 * 100)}pct{ext}"
                combo_img2.save(os.path.join(output_folder, combo_filename2))
                print(f"  -> Created combo image: {combo_filename2}")

        except Exception as e:
            print(f"Error processing image {filename}: {e}")


if __name__ == '__main__':
    input_directory = 'csdi_datasets/croped_images'
    output_directory = 'csdi_datasets/croped_augmented_images'

    if not os.path.isdir(input_directory):
        print(f"Error: input folder '{input_directory}' does not exist or is not a directory.")
    else:
        process_images_ultimate(
            input_directory,
            output_directory,
            rotation_angle_range=15,
            zoom_in_range=(1.05, 1.17)
        )
        print("\nProcessing complete!")
