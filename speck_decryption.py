"""import numpy as np
import cv2

def speck_decrypt(image, key):
    return image ^ key  # XOR decryption (same as encryption)

def decrypt_image(image_path, key_path, output_path):
    encrypted_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    key = np.load(key_path + ".npy")
    decrypted_image = speck_decrypt(encrypted_image, key)
    cv2.imwrite(output_path, decrypted_image)
    print(f"Decrypted image saved as {output_path}")

decrypt_image("encrypted_image.png", "encryption_key", "decrypted_image.png")
"""
"""import numpy as np
import cv2
from speck_cipher import SpeckCipher

def decrypt_image(image_path, key_path, output_path):
    key = np.load(key_path)
    speck = SpeckCipher(key)

    # Read binary file as uint16
    encrypted_data = np.fromfile(image_path, dtype=np.uint16)

    # Debugging size check
    expected_size = 256 * 256
    print(f"🔍 Expected size: {expected_size}, Read size: {encrypted_data.size}")

    if encrypted_data.size != expected_size:
        raise ValueError(f"File size mismatch: Expected {expected_size}, got {encrypted_data.size}")

    encrypted_image = encrypted_data.reshape((256, 256))

    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint16)
    
    for i in range(0, encrypted_image.shape[0] - 1, 2):
        for j in range(encrypted_image.shape[1]):
            decrypted_image[i, j], decrypted_image[i+1, j] = speck.decrypt_block(encrypted_image[i, j], encrypted_image[i+1, j])

    # Convert back to uint8 (scale down)
    decrypted_image = (decrypted_image / 257).astype(np.uint8)

    cv2.imwrite(output_path, decrypted_image)
    print(f"✅ Decrypted image saved as {output_path}")

decrypt_image("encrypted_image.bin", "encryption_key.npy", "decrypted_image.png")
"""
"""import numpy as np
import cv2
from speck_cipher import SPECKCipher

def decrypt_image(image_path, key_path, output_path):
    encrypted_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if encrypted_image is None:
        raise ValueError("Error: Could not load encrypted image.")

    key = np.load(key_path)
    speck = SPECKCipher(key)

    reshaped_encrypted = encrypted_image.reshape(-1, 2).astype(np.uint16)  # Convert to 16-bit words
    left, right = reshaped_encrypted[:, 0], reshaped_encrypted[:, 1]
    decrypted_left, decrypted_right = speck.decrypt_block(left, right)

    decrypted_image = np.column_stack((decrypted_left, decrypted_right)).reshape(256, 256).astype(np.uint8)
    cv2.imwrite(output_path, decrypted_image)

    print(f"Decrypted image saved as {output_path}")

decrypt_image("encrypted_image.png", "encryption_key.npy", "decrypted_image.png")
"""


"""
import numpy as np
import cv2
from speck_cipher import SpeckCipher
import os
import struct

def decrypt_image(encrypted_path, key_path, output_path):
    # Load key
    if not os.path.exists(key_path):
        print(f"Error: Key file {key_path} not found")
        return
    key = np.load(key_path)
    print(f"Using decryption key: {key}")
    
    # Load encrypted image from binary file
    if not os.path.exists(encrypted_path):
        print(f"Error: Encrypted file {encrypted_path} not found")
        return
    
    # Read binary file
    with open(encrypted_path, 'rb') as f:
        # Read header information
        width, height = struct.unpack('II', f.read(8))
        print(f"Image dimensions: {width}x{height}")
        
        # Read pixel data
        encrypted_data = np.fromfile(f, dtype=np.uint16)
        
    # Reshape data to 2D array
    if len(encrypted_data) != width * height:
        print(f"Warning: Data size mismatch. Expected {width*height}, got {len(encrypted_data)}")
        # Adjust if needed
        encrypted_data = encrypted_data[:width*height]
    
    encrypted_image = encrypted_data.reshape((height, width))
    print(f"Encrypted image shape: {encrypted_image.shape}")
    
    # Initialize SPECK cipher with the key
    speck = SpeckCipher(key)

    # Create output array
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint16)
    
    # Decrypt each pair of pixels
    for i in range(0, height - 1, 2):
        for j in range(width):
            try:
                decrypted_image[i, j], decrypted_image[i+1, j] = speck.decrypt_block(
                    int(encrypted_image[i, j]), int(encrypted_image[i+1, j])
                )
            except Exception as e:
                print(f"Error decrypting at position ({i}, {j}): {e}")

    # Convert back to uint8 for saving as an image
    decrypted_image_uint8 = decrypted_image.astype(np.uint8)
    
    # Save the decrypted image
    cv2.imwrite(output_path, decrypted_image_uint8)
    
    # Debug: Save different versions of the image to help diagnose issues
    cv2.imwrite(output_path + ".raw.png", decrypted_image)
    
    print(f"✅ Decrypted image saved as {output_path}")
    print(f"   Debug version saved as {output_path}.raw.png")
    print(f"   Shape: {decrypted_image.shape}, Min: {decrypted_image.min()}, Max: {decrypted_image.max()}")"""


import numpy as np
import cv2
from speck_cipher import SpeckCipher
import os
import struct

def decrypt_image(encrypted_path, key_path, output_path):
    # Load key
    if not os.path.exists(key_path):
        print(f"Error: Key file {key_path} not found")
        return
    key = np.load(key_path)
    print(f"Using decryption key: {key}")
    
    # Load encrypted image from binary file
    if not os.path.exists(encrypted_path):
        print(f"Error: Encrypted file {encrypted_path} not found")
        return
    
    # Read binary file
    with open(encrypted_path, 'rb') as f:
        # Read header information (now includes channels)
        width, height, channels = struct.unpack('III', f.read(12))
        print(f"Image dimensions: {width}x{height}x{channels}")
        
        # Read pixel data
        encrypted_data = np.fromfile(f, dtype=np.uint16)
        
    # Reshape data to 3D array
    if len(encrypted_data) != width * height * channels:
        print(f"Warning: Data size mismatch. Expected {width*height*channels}, got {len(encrypted_data)}")
        # Adjust if needed
        encrypted_data = encrypted_data[:width*height*channels]
    
    encrypted_image = encrypted_data.reshape((height, width, channels))
    print(f"Encrypted image shape: {encrypted_image.shape}")
    
    # Initialize SPECK cipher with the key
    speck = SpeckCipher(key)

    # Create output array
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint16)
    
    # Decrypt each color channel separately
    for c in range(channels):
        # Decrypt each pair of pixels in this channel
        for i in range(0, height - 1, 2):
            for j in range(width):
                try:
                    decrypted_image[i, j, c], decrypted_image[i+1, j, c] = speck.decrypt_block(
                        int(encrypted_image[i, j, c]), int(encrypted_image[i+1, j, c])
                    )
                except Exception as e:
                    print(f"Error decrypting at position ({i}, {j}, {c}): {e}")

    # Convert back to uint8 for saving as an image
    decrypted_image_uint8 = decrypted_image.astype(np.uint8)
    
    # Save the decrypted image
    cv2.imwrite(output_path, decrypted_image_uint8)
    
    print(f"✅ Decrypted color image saved as {output_path}")
    print(f"   Shape: {decrypted_image.shape}, Min: {decrypted_image.min()}, Max: {decrypted_image.max()}")
