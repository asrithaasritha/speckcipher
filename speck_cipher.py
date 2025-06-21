"""import numpy as np
import warnings

class SpeckCipher:
    def __init__(self, key):
        self.key = np.uint16(key)  # Ensure 16-bit key
        self.round_keys = self.key_schedule()

    def key_schedule(self):
        l = [self.key]
        round_keys = []
        for i in range(22):  # Speck-16/32 has 22 rounds
            round_keys.append(l[i])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                l.append(np.uint16((self.right_rotate(l[i], 7) + round_keys[i]) & 0xFFFF) ^ i)
        return round_keys

    def right_rotate(self, x, r):
        return np.uint16((x >> r) | ((x << (16 - r)) & 0xFFFF))  # Ensuring 16-bit result

    def encrypt_block(self, x, y):
        x, y = np.uint16(x), np.uint16(y)  # Ensure 16-bit input
        for k in self.round_keys:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                x = np.uint16((self.right_rotate(x, 7) + y) & 0xFFFF) ^ k
            y = self.right_rotate(y, 2) ^ x
        return x, y

    def decrypt_block(self, x, y):
        x, y = np.uint16(x), np.uint16(y)  # Ensure 16-bit input
        for k in reversed(self.round_keys):
            y = self.right_rotate(y ^ x, 2)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                x = np.uint16((self.right_rotate(x, 9) - y) & 0xFFFF) ^ k
        return x, y"""
"""
import numpy as np
import warnings

warnings.simplefilter("ignore", RuntimeWarning)  # Ignore overflow warnings

class SPECKCipher:
    def __init__(self, key):
        self.key = np.uint16(key).item()  # Ensure the key is a scalar
        self.round_keys = self.expand_key()

    def right_rotate(self, x, r):
        return ((x >> r) | (x << (16 - r))) & 0xFFFF  # Ensure 16-bit operation

    def expand_key(self):
        round_keys = [self.key]
        l = [self.key]
        for i in range(1, 22):  # 22 rounds for Speck-32/64
            temp = ((self.right_rotate(l[i-1], 7) + round_keys[i-1]) & 0xFFFF) ^ i
            l.append(temp)
            round_keys.append(self.right_rotate(round_keys[i-1], 2) ^ l[i])
        return round_keys

    def encrypt_block(self, x, y):
        # Convert numpy values to Python integers
        x = int(np.uint16(x).item())
        y = int(np.uint16(y).item())

        for k in self.round_keys:
            x = ((self.right_rotate(x, 7) + y) & 0xFFFF) ^ k
            y = self.right_rotate(y, 2) ^ x

        return x, y  # Return pure Python integers

    def decrypt_block(self, x, y):
        x = int(np.uint16(x).item())
        y = int(np.uint16(y).item())

        for k in reversed(self.round_keys):
            y = self.right_rotate(y ^ x, 14)
            x = ((x ^ k) - y) & 0xFFFF

        return x, y
"""


"""

import numpy as np

class SpeckCipher:
    def __init__(self, key):
        self.key = np.uint16(key)  # Ensure 16-bit key
        self.rounds = 22  # Speck-16/32 has 22 rounds
        self.round_keys = self.key_schedule()

    def key_schedule(self):
        l = [self.key]
        round_keys = []
        
        for i in range(self.rounds):
            round_keys.append(np.uint16(l[i]))
            # Calculate next round key
            rotated = self.right_rotate(l[i], 7)
            # Handle overflow correctly with explicit modulo
            added = (int(rotated) + int(round_keys[i])) % 65536
            l.append(np.uint16(added ^ i))
            
        return round_keys

    def right_rotate(self, x, r):
        x = int(x) & 0xFFFF  # Ensure 16-bit value
        return np.uint16(((x >> r) | (x << (16 - r))) & 0xFFFF)
    
    def left_rotate(self, x, r):
        x = int(x) & 0xFFFF  # Ensure 16-bit value
        return np.uint16(((x << r) | (x >> (16 - r))) & 0xFFFF)

    def encrypt_block(self, x, y):
        x, y = int(x) & 0xFFFF, int(y) & 0xFFFF
        
        for k in self.round_keys:
            # SPECK round function
            # Handle addition with explicit modulo to avoid overflow
            rotated_x = self.right_rotate(x, 7)
            x = (int(rotated_x) + int(y)) % 65536
            x = x ^ int(k)
            y = int(self.left_rotate(y, 2)) ^ int(x)
            
            # Convert back to uint16
            x, y = np.uint16(x), np.uint16(y)
            
        return x, y

    def decrypt_block(self, x, y):
        x, y = int(x) & 0xFFFF, int(y) & 0xFFFF
        
        for k in reversed(self.round_keys):
            # Convert to integer for calculations to avoid overflow
            k = int(k)
            
            # Inverse SPECK round function
            prev_y = int(y) ^ int(x)
            prev_y = int(self.right_rotate(prev_y, 2))
            
            prev_x = int(x) ^ k
            prev_x = (prev_x - prev_y) % 65536  # Use modulo for correct subtraction
            prev_x = int(self.left_rotate(prev_x, 7))
            
            x, y = np.uint16(prev_x), np.uint16(prev_y)
            
        return x, y"""
import numpy as np

class SpeckCipher:
    def __init__(self, key):
        self.key = np.uint16(key)  # Ensure 16-bit key
        self.rounds = 22  # Speck-16/32 has 22 rounds
        self.round_keys = self.key_schedule()
        
        # Generate T-tables for the full 16-bit space
        self.t_tables = self.generate_t_tables()

    def key_schedule(self):
        """Generate round keys for the SPECK cipher"""
        l = [self.key]
        round_keys = []
        
        for i in range(self.rounds):
            round_keys.append(np.uint16(l[i]))
            # Calculate next round key (using original ARX for key schedule)
            rotated = self.right_rotate(l[i], 7)
            added = (int(rotated) + int(round_keys[i])) % 65536
            l.append(np.uint16(added ^ i))
            
        return round_keys
    
    def right_rotate(self, x, r):
        """Rotate right by r bits within 16-bit space"""
        x = int(x) & 0xFFFF  # Ensure 16-bit value
        return np.uint16(((x >> r) | (x << (16 - r))) & 0xFFFF)
    
    def left_rotate(self, x, r):
        """Rotate left by r bits within 16-bit space"""
        x = int(x) & 0xFFFF  # Ensure 16-bit value
        return np.uint16(((x << r) | (x >> (16 - r))) & 0xFFFF)
    
    def generate_t_tables(self):
        """Generate T-tables for all rounds"""
        # Create a table for each operation needed
        t_rotate_right7 = {}  # x >>> 7
        t_rotate_left2 = {}   # y <<< 2
        t_rotate_right2 = {}  # y >>> 2
        t_rotate_left7 = {}   # x <<< 7
        
        # Precompute all possible values (for 16-bit inputs)
        for i in range(65536):
            t_rotate_right7[i] = int(self.right_rotate(i, 7))
            t_rotate_left2[i] = int(self.left_rotate(i, 2))
            t_rotate_right2[i] = int(self.right_rotate(i, 2))
            t_rotate_left7[i] = int(self.left_rotate(i, 7))
        
        return {
            'right7': t_rotate_right7,
            'left2': t_rotate_left2,
            'right2': t_rotate_right2,
            'left7': t_rotate_left7
        }

    def encrypt_block(self, x, y):
        """Encrypt a pair of 16-bit values using T-tables"""
        x, y = int(x) & 0xFFFF, int(y) & 0xFFFF
        
        for k in self.round_keys:
            # Use T-tables for rotations
            rotated_x = self.t_tables['right7'][x]
            # Still need to do addition and XOR
            x = (rotated_x + y) % 65536
            x = x ^ int(k)
            
            # Use T-table for rotation
            rotated_y = self.t_tables['left2'][y]
            y = rotated_y ^ x
            
        return np.uint16(x), np.uint16(y)

    def decrypt_block(self, x, y):
        """Decrypt a pair of 16-bit values using T-tables"""
        x, y = int(x) & 0xFFFF, int(y) & 0xFFFF
        
        for k in reversed(self.round_keys):
            # Inverse SPECK round function with T-tables
            prev_y = y ^ x
            prev_y = self.t_tables['right2'][prev_y]
            
            prev_x = x ^ int(k)
            prev_x = (prev_x - prev_y) % 65536
            prev_x = self.t_tables['left7'][prev_x]
            
            x, y = prev_x, prev_y
            
        return np.uint16(x), np.uint16(y)