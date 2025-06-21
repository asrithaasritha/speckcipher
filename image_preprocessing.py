"""import cv2
import numpy as np

def preprocess_image(input_path, output_path):
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if image is None:
        print("Error: Could not load image.")
        return
    image = cv2.resize(image, (256, 256))  # Resizing to a fixed size
    cv2.imwrite(output_path, image)
    print(f"Preprocessed image saved as {output_path}")

preprocess_image("D:\DAA_Project\image.png", "processed_image.png")"""
"""import cv2
import numpy as np

def preprocess_image(input_path, output_path):
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale
    if image is None:
        print("Error: Could not load image.")
        return

    image = cv2.resize(image, (128, 128))  # Resize to fixed size
    cv2.imwrite(output_path, image)
    print(f"Preprocessed image saved as {output_path}")

preprocess_image("image.png", "processed_image.png")"""


"""
import cv2
import numpy as np

def preprocess_image(input_path, output_path):
    # Read the image
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)  # Changed to grayscale to match encryption
    if image is None:
        print(f"Error: Could not load image from {input_path}")
        return
    
    # Ensure dimensions are even for proper pair-wise processing
    height, width = 256, 256
    image = cv2.resize(image, (width, height))
    
    # Save the preprocessed image
    cv2.imwrite(output_path, image)
    print(f"Preprocessed image saved as {output_path}")

if __name__ == "__main__":
    preprocess_image("image.png", "processed_image.png")
"""

import cv2
import numpy as np

def preprocess_image(input_path, output_path):
    # Read the image in color
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error: Could not load image from {input_path}")
        return
    
    # Resize image to 256x256
    image = cv2.resize(image, (256, 256))
    
    # Ensure dimensions are even for proper pair-wise processing
    height, width, channels = image.shape
    if height % 2 != 0:
        image = image[:-1, :, :]
    if width % 2 != 0:
        image = image[:, :-1, :]
    
    # Save the preprocessed image
    cv2.imwrite(output_path, image)
    print(f"Preprocessed color image saved as {output_path}")
    return image

if __name__ == "__main__":
    preprocess_image("image.png", "processed_image.png")