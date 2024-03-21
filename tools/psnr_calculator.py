import cv2
import numpy as np


def main():
    # Load original and compressed images
    original_img = cv2.imread(r'/path/to/original/image.png')
    compressed_img = cv2.imread(r'/path/to/compressed/image.png')

    # Convert images to float32 for calculation
    original_img = original_img.astype(np.float32)
    compressed_img = compressed_img.astype(np.float32)

    # Calculate Mean Squared Error (MSE)
    mse = np.mean((original_img - compressed_img) ** 2)

    # Calculate PSNR
    max_pixel_value = 255  # Assuming 8-bit images
    psnr = 10 * np.log10((max_pixel_value ** 2) / mse)

    print("PSNR:", psnr)

if __name__ == "__main__":
    main()