"""import numpy as np
import cv2
def generate_key(image_path, key_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print("Error: Could not load image.")
        return
    key = np.random.randint(0, 256, image.shape, dtype=np.uint8)
    np.save(key_path, key)
    print(f"Key saved as {key_path}.npy")

generate_key("processed_image.png", "encryption_key")"""
"""import numpy as np

def generate_key():
    return np.random.randint(0, 65536, dtype=np.uint16)  # 16-bit key

if __name__ == "__main__":
    key = generate_key()
    np.save("encryption_key.npy", key)
    print(f"Encryption key saved.")
"""
import numpy as np

def generate_key():
    # Generate a single 16-bit key for SPECK cipher
    key = np.random.randint(0, 65536, dtype=np.uint16)
    np.save("encryption_key.npy", key)
    print(f"Key saved as encryption_key.npy (Value: {key})")
    return key

if __name__ == "__main__":
    generate_key()