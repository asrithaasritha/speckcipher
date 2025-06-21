"""import os
import sys
from image_preprocessing import preprocess_image
from key_generation import generate_key
from speck_encryption import encrypt_image
from speck_decryption import decrypt_image

def main():
    # Get input image path
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("Enter path to input image: ")
    
    if not os.path.exists(input_image):
        print(f"Error: Input image {input_image} not found")
        return
    
    # Process the image
    processed_image = "processed_image.png"
    preprocess_image(input_image, processed_image)
    
    # Generate key or use existing one
    key_path = "encryption_key.npy"
    if not os.path.exists(key_path):
        generate_key()
    
    # Encrypt the image
    encrypted_image = "encrypted_image.bin"
    encrypt_image(processed_image, key_path, encrypted_image)
    
    # Decrypt the image
    decrypted_image = "decrypted_image.png"
    decrypt_image(encrypted_image, key_path, decrypted_image)
    
    print("\nSummary:")
    print(f"Original image: {input_image}")
    print(f"Processed image: {processed_image}")
    print(f"Encrypted image: {encrypted_image} (visualization: {encrypted_image}.png)")
    print(f"Decryption key: {key_path}")
    print(f"Decrypted image: {decrypted_image}")

if __name__ == "__main__":
    main()"""
"""

import os
import sys
import time  # Import time module
from image_preprocessing import preprocess_image
from key_generation import generate_key
from speck_encryption import encrypt_image
from speck_decryption import decrypt_image

def main():
    start_time = time.time()  # Start timer

    # Get input image path
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("Enter path to input image: ")
    
    if not os.path.exists(input_image):
        print(f"Error: Input image {input_image} not found")
        return
    
    # Process the image
    processed_image = "processed_image.png"
    preprocess_image(input_image, processed_image)
    
    # Generate key or use existing one
    key_path = "encryption_key.npy"
    if not os.path.exists(key_path):
        generate_key()
    
    # Encrypt the image
    encrypted_image = "encrypted_image.bin"
    encrypt_image(processed_image, key_path, encrypted_image)
    
    # Decrypt the image
    decrypted_image = "decrypted_image.png"
    decrypt_image(encrypted_image, key_path, decrypted_image)

    end_time = time.time()  # End timer
    total_time = end_time - start_time  # Calculate total time

    print("\nSummary:")
    print(f"Original image: {input_image}")
    print(f"Processed image: {processed_image}")
    print(f"Encrypted image: {encrypted_image} (visualization: {encrypted_image}.png)")
    print(f"Decryption key: {key_path}")
    print(f"Decrypted image: {decrypted_image}")
    print(f"⏳ Total execution time: {total_time:.2f} seconds")  # Print total time

if __name__ == "__main__":
    main()
"""
"""
import os
import sys
from image_preprocessing import preprocess_image
from key_generation import generate_key
from speck_encryption import encrypt_image
from speck_decryption import decrypt_image
from image_metrics import calculate_metrics
from encryption_analysis import analyze_encryption_quality

def main():
    # Get input image path
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("Enter path to input image: ")
    
    if not os.path.exists(input_image):
        print(f"Error: Input image {input_image} not found")
        return
    
    # Process the image
    processed_image = "processed_image.png"
    preprocess_image(input_image, processed_image)
    
    # Generate key or use existing one
    key_path = "encryption_key.npy"
    if not os.path.exists(key_path):
        generate_key()
    
    # Encrypt the image
    encrypted_image = "encrypted_image.bin"
    encrypt_image(processed_image, key_path, encrypted_image)
    
    # Decrypt the image
    decrypted_image = "decrypted_image.png"
    decrypt_image(encrypted_image, key_path, decrypted_image)
    
    print("\nSummary:")
    print(f"Original image: {input_image}")
    print(f"Processed image: {processed_image}")
    print(f"Encrypted image: {encrypted_image} (visualization: {encrypted_image}.png)")
    print(f"Decryption key: {key_path}")
    print(f"Decrypted image: {decrypted_image}")
    
    # Perform comprehensive analysis
    print("\nPerforming comprehensive encryption analysis...")
    analyze_encryption_quality(processed_image, encrypted_image, decrypted_image)

if __name__ == "__main__":
    main()
    """

import os
import sys
import shutil
from image_preprocessing import preprocess_image
from key_generation import generate_key
from speck_encryption import encrypt_image
from speck_decryption import decrypt_image
from image_metrics import calculate_metrics
from encryption_analysis import analyze_encryption_quality
from encryption_attack import attack_encrypted_image
from attack_impact_analysis import analyze_attack_impact

def run_normal_scenario(input_image):
    """Run the normal encryption/decryption scenario"""
    print("\n" + "="*50)
    print("SCENARIO 1: NORMAL ENCRYPTION AND DECRYPTION")
    print("="*50)
    
    # Process the image
    processed_image = "processed_image.png"
    preprocess_image(input_image, processed_image)
    
    # Generate key or use existing one
    key_path = "encryption_key.npy"
    if not os.path.exists(key_path):
        generate_key()
    
    # Encrypt the image
    encrypted_image = "encrypted_image.bin"
    encrypt_image(processed_image, key_path, encrypted_image)
    
    # Decrypt the image
    decrypted_image = "decrypted_image.png"
    decrypt_image(encrypted_image, key_path, decrypted_image)
    
    print("\nNormal Scenario Summary:")
    print(f"Original image: {input_image}")
    print(f"Processed image: {processed_image}")
    print(f"Encrypted image: {encrypted_image}")
    print(f"Decryption key: {key_path}")
    print(f"Decrypted image: {decrypted_image}")
    
    # Perform comprehensive analysis
    print("\nPerforming normal encryption analysis...")
    analyze_encryption_quality(processed_image, encrypted_image, decrypted_image)

def run_attack_scenario(input_image, attack_type="block_corruption", severity=0.2):
    """Run the encryption/decryption with attack simulation"""
    print("\n" + "="*50)
    print(f"SCENARIO 2: ENCRYPTION WITH {attack_type.upper()} ATTACK (SEVERITY: {severity*100:.1f}%)")
    print("="*50)
    
    # Copy files from normal scenario
    processed_image = "processed_image.png"
    key_path = "encryption_key.npy"
    encrypted_image = "encrypted_image.bin"
    
    # Check if files exist from previous scenario
    if not all(os.path.exists(f) for f in [processed_image, key_path, encrypted_image]):
        print("Error: Files from normal scenario not found. Run normal scenario first.")
        return
    
    # Attack the encrypted image
    attacked_image = "attacked_image.bin"
    if not attack_encrypted_image(encrypted_image, attacked_image, attack_type, severity):
        print("Attack simulation failed!")
        return
    
    # Copy visualization
    if os.path.exists(encrypted_image + '.png'):
        shutil.copy(encrypted_image + '.png', attacked_image + '.png')
    
    # Decrypt the attacked image
    attacked_decrypted = "attacked_decrypted.png"
    decrypt_image(attacked_image, key_path, attacked_decrypted)
    
    print("\nAttack Scenario Summary:")
    print(f"Original image: {input_image}")
    print(f"Processed image: {processed_image}")
    print(f"Encrypted image: {encrypted_image}")
    print(f"Attacked encrypted image: {attacked_image}")
    print(f"Decryption key: {key_path}")
    print(f"Decrypted attacked image: {attacked_decrypted}")
    
    # Perform comprehensive analysis
    print("\nPerforming attacked encryption analysis...")
    analyze_encryption_quality(processed_image, attacked_image, attacked_decrypted)
    
    # Perform attack impact analysis
    print("\nPerforming attack impact analysis...")
    normal_decrypted = "decrypted_image.png"
    analyze_attack_impact(processed_image, normal_decrypted, attacked_decrypted)

def main():
    # Get input image path
    if len(sys.argv) > 1:
        input_image = sys.argv[1]
    else:
        input_image = input("Enter path to input image: ")
    
    if not os.path.exists(input_image):
        print(f"Error: Input image {input_image} not found")
        return
    
    # Get attack parameters if specified
    attack_type = "block_corruption"
    severity = 0.2
    
    if len(sys.argv) > 2:
        attack_type = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            severity = float(sys.argv[3])
            if not 0 <= severity <= 1:
                print("Severity must be between 0.0 and 1.0. Using default 0.2.")
                severity = 0.2
        except ValueError:
            print("Invalid severity value. Using default 0.2.")
            severity = 0.2
    
    # Run normal scenario
    run_normal_scenario(input_image)
    
    # Run attack scenario
    run_attack_scenario(input_image, attack_type, severity)
    
    print("\n" + "="*50)
    print("COMPLETE! Both scenarios have been executed.")
    print("="*50)
    print("Files generated:")
    print("- processed_image.png: The preprocessed original image")
    print("- encrypted_image.bin: The normal encrypted image")
    print("- decrypted_image.png: The normal decrypted image")
    print("- attacked_image.bin: The attacked encrypted image")
    print("- attacked_decrypted.png: The decrypted image after attack")
    print("- encryption_analysis.png: Analysis of normal encryption")
    print("- attack_impact_analysis.png: Analysis of the attack impact")
    
    print("\nTo run with different attack parameters, use:")
    print(f"python {sys.argv[0]} <image_path> <attack_type> <severity>")
    print("Attack types: noise, bitflip, block_corruption")
    print("Severity: 0.0-1.0 (higher values cause more damage)")

if __name__ == "__main__":
    main()