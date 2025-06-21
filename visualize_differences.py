import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

def visualize_differences(original_path, compared_path, output_path="difference_visualization.png"):
    """
    Create a visualization showing the original, decrypted, and difference images
    """
    # Load images
    original = cv2.imread(original_path)
    compared = cv2.imread(compared_path)
    
    if original is None or compared is None:
        print(f"Error: Could not load images")
        return
    
    # Ensure both images have same dimensions
    if original.shape != compared.shape:
        compared = cv2.resize(compared, (original.shape[1], original.shape[0]))
    
    # Convert BGR to RGB for matplotlib display
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    compared_rgb = cv2.cvtColor(compared, cv2.COLOR_BGR2RGB)
    
    # Calculate SSIM and difference image (multichannel for color images)
    gray_original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_compared = cv2.cvtColor(compared, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(gray_original, gray_compared, full=True)
    
    # The diff image contains the actual values in the range [-1, 1]
    # We need to convert it to the range [0, 255] for display
    diff = (diff * 255).astype("uint8")
    
    # Calculate absolute difference image for better visualization
    abs_diff = cv2.absdiff(original, compared)
    # Enhance the difference for visualization
    abs_diff = cv2.convertScaleAbs(abs_diff, alpha=5)  # Multiply by 5 to make differences more visible
    
    # Create heatmap of differences
    heatmap = cv2.applyColorMap(abs_diff, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Compute pixel-wise difference statistics
    mean_diff = np.mean(abs_diff)
    max_diff = np.max(abs_diff)
    
    # Create figure
    plt.figure(figsize=(15, 10))
    
    # Original image
    plt.subplot(2, 2, 1)
    plt.imshow(original_rgb)
    plt.title('Original Image')
    plt.axis('off')
    
    # Decrypted image
    plt.subplot(2, 2, 2)
    plt.imshow(compared_rgb)
    plt.title('Decrypted Image')
    plt.axis('off')
    
    # Difference map
    plt.subplot(2, 2, 3)
    plt.imshow(diff, cmap='gray')
    plt.title(f'SSIM Difference Map (Score: {score:.4f})')
    plt.axis('off')
    
    # Heatmap visualization
    plt.subplot(2, 2, 4)
    plt.imshow(heatmap_rgb)
    plt.title(f'Difference Heatmap (Mean: {mean_diff:.2f}, Max: {max_diff})')
    plt.axis('off')
    
    # Add text with metrics
    plt.figtext(0.5, 0.02, f"SSIM Score: {score:.4f} (1.0 = perfect match)\nMean Absolute Difference: {mean_diff:.2f}\nMaximum Absolute Difference: {max_diff}", 
                ha="center", fontsize=12, bbox={"facecolor":"white", "alpha":0.8, "pad":5})
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Difference visualization saved as {output_path}")
    
    # Display figure (optional, may not work in all environments)
    try:
        plt.show()
    except Exception as e:
        print(f"Could not display figure: {e}")

if __name__ == "__main__":
    # Example usage
    visualize_differences("processed_image.png", "decrypted_image.png")