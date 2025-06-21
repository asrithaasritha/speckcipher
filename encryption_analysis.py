import os
import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from image_metrics import calculate_metrics
from visualize_differences import visualize_differences

def analyze_encryption_quality(original_path, encrypted_path, decrypted_path):
    """
    Perform a comprehensive analysis of the encryption and decryption process
    """
    # Check if files exist
    for path in [original_path, encrypted_path, decrypted_path]:
        if not os.path.exists(path):
            print(f"Error: File {path} not found")
            return
    
    # Load images
    original = cv2.imread(original_path)
    encrypted_viz = cv2.imread(encrypted_path + '.png')  # Visualization of encrypted image
    decrypted = cv2.imread(decrypted_path)
    
    # Calculate metrics between original and decrypted
    metrics = calculate_metrics(original_path, decrypted_path)
    
    # Calculate histogram of original and encrypted images
    original_hist = []
    encrypted_hist = []
    
    for i in range(3):  # RGB channels
        hist_orig = cv2.calcHist([original], [i], None, [256], [0, 256])
        original_hist.append(hist_orig)
        
        hist_enc = cv2.calcHist([encrypted_viz], [i], None, [256], [0, 256])
        encrypted_hist.append(hist_enc)
    
    # Create visualization of the differences
    visualize_differences(original_path, decrypted_path)
    
    # Create histograms comparison figure
    plt.figure(figsize=(15, 10))
    colors = ('b', 'g', 'r')
    
    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(2, 3, 2)
    plt.imshow(cv2.cvtColor(encrypted_viz, cv2.COLOR_BGR2RGB))
    plt.title('Encrypted Image (Visualization)')
    plt.axis('off')
    
    plt.subplot(2, 3, 3)
    plt.imshow(cv2.cvtColor(decrypted, cv2.COLOR_BGR2RGB))
    plt.title('Decrypted Image')
    plt.axis('off')
    
    # Plot original image histogram
    plt.subplot(2, 3, 4)
    for i, color in enumerate(colors):
        plt.plot(original_hist[i], color=color)
    plt.title('Original Image Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.xlim([0, 256])
    
    # Plot encrypted image histogram
    plt.subplot(2, 3, 5)
    for i, color in enumerate(colors):
        plt.plot(encrypted_hist[i], color=color)
    plt.title('Encrypted Image Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.xlim([0, 256])
    
    # Add metrics summary
    metrics_text = ""
    if metrics:
        metrics_text += f"SSIM: {metrics['SSIM']:.4f} (1.0 = perfect similarity)\n"
        metrics_text += f"MSE: {metrics['MSE']:.2f} (0 = perfect match)\n"
        metrics_text += f"PSNR: {metrics['PSNR']:.2f} dB (higher is better)\n"
        metrics_text += f"Dice Similarity: {metrics['Dice']:.4f} (1.0 = perfect overlap)"
    
    plt.subplot(2, 3, 6)
    plt.text(0.1, 0.5, metrics_text, fontsize=12)
    plt.axis('off')
    plt.title('Image Quality Metrics')
    
    # Save the analysis
    plt.tight_layout()
    plt.savefig("encryption_analysis.png", dpi=300)
    
    # Print metrics summary
    print("\nEncryption Analysis Summary:")
    if metrics:
        print(f"SSIM: {metrics['SSIM']:.4f} (1.0 = perfect similarity)")
        print(f"MSE: {metrics['MSE']:.2f} (0 = perfect match)")
        print(f"PSNR: {metrics['PSNR']:.2f} dB (higher is better)")
        print(f"Dice Similarity: {metrics['Dice']:.4f} (1.0 = perfect overlap)")
        
        # Interpret the results
        if metrics['SSIM'] > 0.95:
            print("\nInterpretation: Excellent decryption quality! The decrypted image is nearly identical to the original.")
        elif metrics['SSIM'] > 0.85:
            print("\nInterpretation: Good decryption quality. Minor differences may be present but not significant.")
        elif metrics['SSIM'] > 0.7:
            print("\nInterpretation: Fair decryption quality. Some noticeable differences exist.")
        else:
            print("\nInterpretation: Poor decryption quality. Significant differences detected.")
    else:
        print("Unable to calculate metrics.")
    
    print(f"\nVisualization saved as encryption_analysis.png")
    print(f"Detailed difference visualization saved as difference_visualization.png")

if __name__ == "__main__":
    # Get paths from command line or use defaults
    if len(sys.argv) > 3:
        original = sys.argv[1]
        encrypted = sys.argv[2]
        decrypted = sys.argv[3]
    else:
        original = "processed_image.png"
        encrypted = "encrypted_image.bin"
        decrypted = "decrypted_image.png"
    
    analyze_encryption_quality(original, encrypted, decrypted)