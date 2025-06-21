import os
import sys
import time
import numpy as np
import cv2
import struct

class SpeckCipher:
    """SPECK Cipher implementation for 16-bit encryption."""

    def __init__(self, key):
        self.key = np.uint16(key)
        self.rounds = 22
        self.round_keys = self.key_schedule()

    def key_schedule(self):
        """Generates round keys for SPECK encryption while handling uint16 overflow."""
        l = [self.key]
        round_keys = []

        for i in range(self.rounds):
            round_keys.append(np.uint16(l[i]))
            rotated = self.right_rotate(l[i], 7)
            new_l = np.uint16((rotated + round_keys[i]) ^ i)  # Prevent overflow
            l.append(new_l)

        return round_keys

    @staticmethod
    def right_rotate(x, r):
        return np.uint16((x >> r) | (x << (16 - r)) & 0xFFFF)

    @staticmethod
    def left_rotate(x, r):
        return np.uint16((x << r) | (x >> (16 - r)) & 0xFFFF)

    def encrypt_block(self, x, y):
        """Encrypts a pair of 16-bit values using SPECK."""
        x, y = np.uint16(x), np.uint16(y)
        for k in self.round_keys:
            x = self.right_rotate(x, 7)
            x = np.uint16((x + y) % 65536) ^ k
            y = self.left_rotate(y, 2) ^ x
        return x, y

    def decrypt_block(self, x, y):
        """Decrypts a pair of 16-bit values using SPECK."""
        x, y = np.uint16(x), np.uint16(y)
        for k in reversed(self.round_keys):
            y = self.right_rotate(y ^ x, 2)
            x = np.uint16((self.left_rotate(x ^ k, 9) - y) % 65536)
        return x, y

def preprocess_image(input_image_path, output_image_path):
    """Resizes image to 256x256 and ensures even dimensions."""
    image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"❌ Error: Could not load image from {input_image_path}")

    image = cv2.resize(image, (256, 256))
    cv2.imwrite(output_image_path, image)

def generate_key(key_path="encryption_key.npy"):
    """Generates and saves a 16-bit encryption key."""
    key = np.random.randint(0, 65536, dtype=np.uint16)
    np.save(key_path, key)
    print(f"🔑 New key generated: {key}")

def encrypt_image(image_path, key_path, output_path):
    """Encrypts an image using SPECK cipher and saves to a binary file."""
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"❌ Error: Could not load image from {image_path}")

    image = image.astype(np.uint16)
    height, width, channels = image.shape

    key = np.load(key_path).item()
    speck = SpeckCipher(key)

    encrypted_image = np.copy(image)  # Avoid modifying original image

    for c in range(channels):
        for i in range(0, height - 1, 2):
            for j in range(width):
                encrypted_image[i, j, c], encrypted_image[i+1, j, c] = speck.encrypt_block(
                    image[i, j, c], image[i+1, j, c]
                )

    with open(output_path, 'wb') as f:
        f.write(struct.pack('III', width, height, channels))
        encrypted_image.tofile(f)

    cv2.imwrite(output_path + ".png", (encrypted_image % 256).astype(np.uint8))

def decrypt_image(encrypted_path, key_path, output_path):
    """Decrypts an image from binary file using SPECK cipher."""
    if not os.path.exists(encrypted_path) or not os.path.exists(key_path):
        raise ValueError("❌ Error: Encrypted file or key file not found")

    key = np.load(key_path).item()
    speck = SpeckCipher(key)

    with open(encrypted_path, 'rb') as f:
        width, height, channels = struct.unpack('III', f.read(12))
        encrypted_data = np.fromfile(f, dtype=np.uint16)

    encrypted_image = encrypted_data.reshape((height, width, channels))
    decrypted_image = np.copy(encrypted_image)  # Avoid modifying original

    for c in range(channels):
        for i in range(0, height - 1, 2):
            for j in range(width):
                decrypted_image[i, j, c], decrypted_image[i+1, j, c] = speck.decrypt_block(
                    encrypted_image[i, j, c], encrypted_image[i+1, j, c]
                )

    cv2.imwrite(output_path, decrypted_image.astype(np.uint8))

def main():
    """Main function to preprocess, encrypt, and decrypt an image."""
    start_time = time.time()

    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("Enter path to input image: ")

    if not os.path.exists(input_image):
        print(f"❌ Error: Input image {input_image} not found")
        return

    processed_image = "processed_image.png"
    preprocess_image(input_image, processed_image)

    key_path = "encryption_key.npy"
    generate_key(key_path)

    encrypted_image = "encrypted_image.bin"
    encrypt_image(processed_image, key_path, encrypted_image)

    decrypted_image = "decrypted_image.png"
    decrypt_image(encrypted_image, key_path, decrypted_image)

    print(f"\n✅ Encryption & Decryption Completed in {time.time() - start_time:.2f} seconds")
    print(f"➡ Processed: {processed_image}, Encrypted: {encrypted_image}, Decrypted: {decrypted_image}")

if __name__ == "__main__":
    main()
