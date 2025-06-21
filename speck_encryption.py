"""import numpy as np
import cv2

def speck_encrypt(image, key):
    return image ^ key  # Simple XOR encryption with the key

def encrypt_image(image_path, key_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    key = np.load(key_path + ".npy")
    encrypted_image = speck_encrypt(image, key)
    cv2.imwrite(output_path, encrypted_image)
    print(f"Encrypted image saved as {output_path}")

encrypt_image("processed_image.png", "encryption_key", "encrypted_image.png")"""
"""import numpy as np
import cv2
from speck_cipher import SpeckCipher

def encrypt_image(image_path, key_path, output_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Could not load image.")
        return

    # Resize image to 256x256
    image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)

    # Convert to uint16 (scale up from 0-255 to 0-65535)
    image = image.astype(np.uint16) * 257  

    key = np.random.randint(0, 65536, dtype=np.uint16)
    np.save(key_path, key)

    speck = SpeckCipher(key)

    encrypted_image = np.zeros_like(image, dtype=np.uint16)
    
    for i in range(0, image.shape[0] - 1, 2):
        for j in range(image.shape[1]):
            encrypted_image[i, j], encrypted_image[i+1, j] = speck.encrypt_block(image[i, j], image[i+1, j])

    # Save as pure uint16 binary file (ensures correct size)
    encrypted_image.tofile(output_path)  
    print(f"✅ Encrypted image saved as {output_path} (Size: {encrypted_image.size * 2} bytes)")

encrypt_image("image.png", "encryption_key.npy", "encrypted_image.bin")"""
"""
import numpy as np
from speck_cipher import SPECKCipher
from PIL import Image

def encrypt_image(image_path, key_path, output_path):
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    img = img.resize((256, 256))  # Ensure 256x256 size
    img_array = np.array(img, dtype=np.uint16)

    key = np.load(key_path)
    speck = SPECKCipher(key)

    encrypted_image = np.zeros_like(img_array, dtype=np.uint16)

    for i in range(0, 256, 2):
        for j in range(256):
            left = int(img_array[i, j].item())   # Ensure scalar
            right = int(img_array[i+1, j].item()) # Ensure scalar

            el, er = speck.encrypt_block(left, right)

            encrypted_image[i, j] = np.uint16(el)  # Ensure correct type
            encrypted_image[i+1, j] = np.uint16(er)

    encrypted_img = Image.fromarray(encrypted_image.astype(np.uint8))
    encrypted_img.save(output_path)

encrypt_image("image.png", "encryption_key.npy", "encrypted_image.png")
"""


"""
import numpy as np
import cv2
from speck_cipher import SpeckCipher
import os
import struct

def encrypt_image(image_path, key_path, output_path):
    # Read image as grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    # Resize image to 256x256
    image = cv2.resize(image, (256, 256))
    
    # Ensure image dimensions are even
    height, width = image.shape
    if height % 2 != 0:
        image = image[:-1, :]
    if width % 2 != 0:
        image = image[:, :-1]
    
    # Convert to uint16 (original 8-bit values)
    image = image.astype(np.uint16)

    # Load or generate key
    if os.path.exists(key_path):
        key = np.load(key_path)
    else:
        key = np.random.randint(0, 65536, dtype=np.uint16)
        np.save(key_path, key)
    
    print(f"Using encryption key: {key}")
    speck = SpeckCipher(key)

    # Create output array
    encrypted_image = np.zeros_like(image, dtype=np.uint16)
    
    # Encrypt each pair of pixels
    for i in range(0, height - 1, 2):
        for j in range(width):
            encrypted_image[i, j], encrypted_image[i+1, j] = speck.encrypt_block(
                int(image[i, j]), int(image[i+1, j])
            )
    
    # Write encrypted image to binary file
    with open(output_path, 'wb') as f:
        # Write header information (width, height)
        f.write(struct.pack('II', width, height))
        
        # Write pixel data
        encrypted_image.tofile(f)
    
    # Also save as an image for visualization
    cv2.imwrite(output_path + '.png', (encrypted_image % 256).astype(np.uint8))
    
    print(f"✅ Encrypted image saved as {output_path} (Size: {os.path.getsize(output_path)} bytes)")
    print(f"   Visualization saved as {output_path}.png")
    print(f"   Shape: {encrypted_image.shape}, Min: {encrypted_image.min()}, Max: {encrypted_image.max()}")"""
""


import numpy as np
import cv2
from speck_cipher import SpeckCipher
import os
import struct

def encrypt_image(image_path, key_path, output_path):
    # Read image in color
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return

    # Resize image to 256x256
    image = cv2.resize(image, (256, 256))
    
    # Ensure image dimensions are even
    height, width, channels = image.shape
    if height % 2 != 0:
        image = image[:-1, :, :]
    if width % 2 != 0:
        image = image[:, :-1, :]
    
    # Convert to uint16 (original 8-bit values)
    image = image.astype(np.uint16)

    # Load or generate key
    if os.path.exists(key_path):
        key = np.load(key_path)
    else:
        key = np.random.randint(0, 65536, dtype=np.uint16)
        np.save(key_path, key)
    
    print(f"Using encryption key: {key}")
    speck = SpeckCipher(key)

    # Create output array
    encrypted_image = np.zeros_like(image, dtype=np.uint16)
    
    # Encrypt each color channel separately
    for c in range(channels):
        # Encrypt each pair of pixels in this channel
        for i in range(0, height - 1, 2):
            for j in range(width):
                encrypted_image[i, j, c], encrypted_image[i+1, j, c] = speck.encrypt_block(
                    int(image[i, j, c]), int(image[i+1, j, c])
                )
    
    # Write encrypted image to binary file
    with open(output_path, 'wb') as f:
        # Write header information (width, height, channels)
        f.write(struct.pack('III', width, height, channels))
        
        # Write pixel data
        encrypted_image.tofile(f)
    
    # Create a visualization by combining all channels
    visualization = np.zeros((height, width, 3), dtype=np.uint8)
    for c in range(channels):
        visualization[:, :, c] = (encrypted_image[:, :, c] % 256).astype(np.uint8)
    
    cv2.imwrite(output_path + '.png', visualization)
    
    print(f"✅ Encrypted color image saved as {output_path} (Size: {os.path.getsize(output_path)} bytes)")
    print(f"   Visualization saved as {output_path}.png")
    print(f"   Shape: {encrypted_image.shape}, Min: {encrypted_image.min()}, Max: {encrypted_image.max()}")
