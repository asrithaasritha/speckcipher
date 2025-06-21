import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from image_metrics import calculate_metrics
import os

def analyze_attack_impact(original_path, normal_decrypted_path, attacked_decrypted_path, 
                         output_path="attack_impact_analysis.png"):
    """
    Analyze and visualize the impact of the attack by comparing normal and attacked decryption
    """
    # Check if files exist
    if not all(os.path.exists(f) for f in [original_path, normal_decrypted_path, attacked_decrypted_path]):
        print("Error: Required files not found.")
        return
    
    # Load images
    original = cv2.imread(original_path)
    normal = cv2.imread(normal_decrypted_path)
    attacked = cv2.imread(attacked_decrypted_path)
    
    # Convert to RGB for display
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    normal_rgb = cv2.cvtColor(normal, cv2.COLOR_BGR2RGB)
    attacked_rgb = cv2.cvtColor(attacked, cv2.COLOR_BGR2RGB)
    
    # Calculate difference images
    diff_normal = cv2.absdiff(original, normal)
    diff_attacked = cv2.absdiff(original, attacked)
    diff_comparison = cv2.absdiff(normal, attacked)
    
    # Enhance differences for visualization
    diff_normal_enhanced = cv2.convertScaleAbs(diff_normal, alpha=5)
    diff_attacked_enhanced = cv2.convertScaleAbs(diff_attacked, alpha=5)
    diff_comparison_enhanced = cv2.convertScaleAbs(diff_comparison, alpha=5)
    
    # Calculate metrics
    metrics_normal = calculate_metrics(original_path, normal_decrypted_path)
    metrics_attacked = calculate_metrics(original_path, attacked_decrypted_path)
    metrics_comparison = calculate_metrics(normal_decrypted_path, attacked_decrypted_path)
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    
    # Row 1: Images
    plt.subplot(3, 3, 1)
    plt.imshow(original_rgb)
    plt.title('Original Image')
    plt.axis('off')
    
    plt.subplot(3, 3, 2)
    plt.imshow(normal_rgb)
    plt.title('Normal Decryption')
    plt.axis('off')
    
    plt.subplot(3, 3, 3)
    plt.imshow(attacked_rgb)
    plt.title('Attacked Decryption')
    plt.axis('off')
    
    # Row 2: Difference images
    plt.subplot(3, 3, 4)
    plt.imshow(cv2.cvtColor(diff_normal_enhanced, cv2.COLOR_BGR2RGB))
    plt.title('Original vs Normal Decryption\nDifference (Enhanced)')
    plt.axis('off')
    
    plt.subplot(3, 3, 5)
    plt.imshow(cv2.cvtColor(diff_attacked_enhanced, cv2.COLOR_BGR2RGB))
    plt.title('Original vs Attacked Decryption\nDifference (Enhanced)')
    plt.axis('off')
    
    plt.subplot(3, 3, 6)
    plt.imshow(cv2.cvtColor(diff_comparison_enhanced, cv2.COLOR_BGR2RGB))
    plt.title('Normal vs Attacked Decryption\nDifference (Enhanced)')
    plt.axis('off')
    
    # Row 3: Heatmaps
    plt.subplot(3, 3, 7)
    heatmap1 = cv2.applyColorMap(diff_normal_enhanced, cv2.COLORMAP_JET)
    plt.imshow(cv2.cvtColor(heatmap1, cv2.COLOR_BGR2RGB))
    plt.title('Original vs Normal\nHeatmap')
    plt.axis('off')
    
    plt.subplot(3, 3, 8)
    heatmap2 = cv2.applyColorMap(diff_attacked_enhanced, cv2.COLORMAP_JET)
    plt.imshow(cv2.cvtColor(heatmap2, cv2.COLOR_BGR2RGB))
    plt.title('Original vs Attacked\nHeatmap')
    plt.axis('off')
    
    plt.subplot(3, 3, 9)
    heatmap3 = cv2.applyColorMap(diff_comparison_enhanced, cv2.COLORMAP_JET)
    plt.imshow(cv2.cvtColor(heatmap3, cv2.COLOR_BGR2RGB))
    plt.title('Normal vs Attacked\nHeatmap')
    plt.axis('off')
    
    # Add metrics text
    metrics_text = "Metrics Summary:\n\n"
    metrics_text += "Original vs Normal Decryption:\n"
    if metrics_normal:
        metrics_text += f"SSIM: {metrics_normal['SSIM']:.4f}\n"
        metrics_text += f"PSNR: {metrics_normal['PSNR']:.2f} dB\n\n"
    
    metrics_text += "Original vs Attacked Decryption:\n"
    if metrics_attacked:
        metrics_text += f"SSIM: {metrics_attacked['SSIM']:.4f}\n"
        metrics_text += f"PSNR: {metrics_attacked['PSNR']:.2f} dB\n\n"
    
    metrics_text += "Normal vs Attacked Decryption:\n"
    if metrics_comparison:
        metrics_text += f"SSIM: {metrics_comparison['SSIM']:.4f}\n"
        metrics_text += f"PSNR: {metrics_comparison['PSNR']:.2f} dB"
    
    plt.figtext(0.5, 0.01, metrics_text, ha="center", fontsize=9, 
                bbox={"facecolor":"white", "alpha":0.8, "pad":5})
    
    # Save figure
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # Make room for the text
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Attack impact analysis saved as {output_path}")
    
    # Calculate attack effectiveness
    if metrics_normal and metrics_attacked:
        attack_effect = (1 - metrics_attacked['SSIM'] / metrics_normal['SSIM']) * 100
        print(f"\nAttack Impact Assessment:")
        print(f"Normal Decryption SSIM: {metrics_normal['SSIM']:.4f}")
        print(f"Attacked Decryption SSIM: {metrics_attacked['SSIM']:.4f}")
        print(f"Attack Effectiveness: {attack_effect:.2f}% degradation in image quality")
        
        if attack_effect < 5:
            print("Interpretation: The attack had minimal impact on the decrypted image.")
        elif attack_effect < 20:
            print("Interpretation: The attack had a noticeable but limited impact on the decrypted image.")
        elif attack_effect < 50:
            print("Interpretation: The attack had a significant impact on the decrypted image.")
        else:
            print("Interpretation: The attack had a severe impact on the decrypted image.")

if __name__ == "__main__":
    analyze_attack_impact("processed_image.png", "decrypted_image.png", "attacked_decrypted.png")