import numpy as np
import os
import struct
import random

def attack_encrypted_image(encrypted_path, attacked_path, attack_type="noise", severity=0.1):
    """
    Simulate an attack on the encrypted image data
    
    Parameters:
    - encrypted_path: Path to the original encrypted image
    - attacked_path: Path to save the attacked encrypted image
    - attack_type: Type of attack to simulate (noise, bitflip, block_corruption)
    - severity: How severe the attack should be (0.0 to 1.0)
    """
    # Check if file exists
    if not os.path.exists(encrypted_path):
        print(f"Error: Encrypted file {encrypted_path} not found")
        return False
    
    # Read binary file
    with open(encrypted_path, 'rb') as f:
        # Read header information
        header_data = f.read(12)  # 3 uint32 values for width, height, channels
        width, height, channels = struct.unpack('III', header_data)
        print(f"Image dimensions: {width}x{height}x{channels}")
        
        # Read pixel data
        encrypted_data = np.fromfile(f, dtype=np.uint16)
    
    # Make a copy of the data
    attacked_data = encrypted_data.copy()
    data_size = len(attacked_data)
    
    # Calculate number of bytes to corrupt based on severity
    num_to_corrupt = int(data_size * severity)
    print(f"Attacking {num_to_corrupt} values out of {data_size} ({severity*100:.1f}%)")
    
    # Perform different types of attacks
    if attack_type == "noise":
        # Add random noise to selected pixels
        indices = random.sample(range(data_size), num_to_corrupt)
        for idx in indices:
            # Add random noise in the range [-5000, 5000]
            noise = random.randint(-5000, 5000)
            attacked_data[idx] = np.uint16(min(max(int(attacked_data[idx]) + noise, 0), 65535))
    
    elif attack_type == "bitflip":
        # Flip random bits in selected pixels
        indices = random.sample(range(data_size), num_to_corrupt)
        for idx in indices:
            # Select a random bit to flip (0-15 for uint16)
            bit_to_flip = random.randint(0, 15)
            # Flip the bit
            attacked_data[idx] = np.uint16(int(attacked_data[idx]) ^ (1 << bit_to_flip))
    
    elif attack_type == "block_corruption":
        # Corrupt entire blocks of the image
        num_blocks = min(5, int(severity * 20) + 1)  # Scale blocks with severity
        
        for _ in range(num_blocks):
            # Select a random starting point
            if data_size > width * 10:  # Ensure we have enough data
                start_idx = random.randint(0, data_size - width * 10)
                block_size = random.randint(width * 2, width * 10)
                
                # Either randomize the block or set it to a fixed value
                if random.choice([True, False]):
                    attacked_data[start_idx:start_idx+block_size] = np.random.randint(
                        0, 65536, size=block_size, dtype=np.uint16)
                else:
                    attacked_data[start_idx:start_idx+block_size] = np.uint16(random.randint(0, 65535))
    
    else:
        print(f"Unknown attack type: {attack_type}")
        return False
    
    # Write attacked encrypted image to binary file
    with open(attacked_path, 'wb') as f:
        # Write header information (width, height, channels)
        f.write(header_data)
        
        # Write modified pixel data
        attacked_data.tofile(f)
    
    print(f"✅ Attacked encrypted image saved as {attacked_path}")
    print(f"   Attack type: {attack_type}, Severity: {severity*100:.1f}%")
    
    return True

if __name__ == "__main__":
    # Example usage
    attack_encrypted_image("encrypted_image.bin", "attacked_image.bin", 
                          attack_type="block_corruption", severity=0.2)