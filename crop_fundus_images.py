import cv2
import numpy as np
import os
import argparse
from tqdm import tqdm
import csv

def crop_and_save_image(input_path, output_path, padding=10):
    """
    Crop a single fundus image to remove black background and save to the specified path.

    Returns:
        dict: A dictionary containing cropping information, used for writing to CSV.
    """
    try:
        image = cv2.imread(input_path)
        if image is None:
            print(f"Warning: Unable to read image {input_path}, skipped.")
            return None

        original_h, original_w = image.shape[:2]

        # Convert to grayscale for thresholding
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print(f"Warning: No contours found in image {input_path}, skipped.")
            return None

        # Find the largest contour (main fundus region)
        main_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(main_contour)

        img_h, img_w = original_h, original_w
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img_w, x + w + padding)
        y2 = min(img_h, y + h + padding)

        cropped_image = image[y1:y2, x1:x2]

        # Replace white spots in black background with black
        white_mask = np.all(cropped_image == [255, 255, 255], axis=-1)
        cropped_image[white_mask] = [0, 0, 0]

        cv2.imwrite(output_path, cropped_image)

        # Calculate cropped pixels (left, top, right, bottom)
        left_crop = x1
        top_crop = y1
        right_crop = img_w - x2
        bottom_crop = img_h - y2

        return {
            "filename": os.path.basename(input_path),
            "original_width": original_w,
            "original_height": original_h,
            "left_crop": left_crop,
            "top_crop": top_crop,
            "right_crop": right_crop,
            "bottom_crop": bottom_crop
        }

    except Exception as e:
        print(f"Error processing file {input_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Automatically crop fundus images to remove black background.")
    parser.add_argument('-i', '--input_dir', help="Input directory containing original images.", default="csdi_datasets/original_images")
    parser.add_argument('-o', '--output_dir', help="Output directory for saving cropped images.", default="csdi_datasets/croped_images")
    parser.add_argument('-p', '--padding', type=int, default=0, help="Extra pixel padding around the crop boundary, default 0.")
    parser.add_argument('-c', '--csv_path', type=str, default="crop_info.csv", help="CSV file path to save cropping information, default 'crop_info.csv'.")

    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    padding = args.padding
    csv_path = args.csv_path

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)
    print(f"Cropped images will be saved to: '{output_dir}'")

    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]

    if not image_files:
        print(f"No supported image files found in directory '{input_dir}'.")
        return

    crop_records = []

    print(f"Found {len(image_files)} images, starting processing...")
    for filename in tqdm(image_files, desc="Processing progress"):
        input_image_path = os.path.join(input_dir, filename)
        output_image_path = os.path.join(output_dir, filename)

        record = crop_and_save_image(input_image_path, output_image_path, padding)
        if record:
            crop_records.append(record)

    # Write CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["filename", "original_width", "original_height", "left_crop", "top_crop", "right_crop", "bottom_crop"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rec in crop_records:
            writer.writerow(rec)

    print(f"All images processed! Cropping information saved to '{csv_path}'.")

if __name__ == '__main__':
    main()
