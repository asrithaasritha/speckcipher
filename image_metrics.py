import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

def calculate_metrics(original_path, compared_path):
    """Calculate quality metrics between original and compared image"""
    # Load images
    original = cv2.imread(original_path)
    compared = cv2.imread(compared_path)
    
    if original is None or compared is None:
        print(f"Error: Could not load images")
        return None
    
    # Ensure both images have same dimensions
    if original.shape != compared.shape:
        compared = cv2.resize(compared, (original.shape[1], original.shape[0]))
    
    # Calculate SSIM for each channel then average
    ssim_value = 0
    for i in range(3):  # RGB channels
        ssim_channel = ssim(original[:,:,i], compared[:,:,i], 
                             data_range=compared[:,:,i].max() - compared[:,:,i].min())
        ssim_value += ssim_channel
    ssim_value /= 3  # Average across channels
    
    # Calculate MSE
    mse_value = mse(original, compared)
    
    # Calculate PSNR (Peak Signal-to-Noise Ratio)
    if mse_value == 0:
        psnr_value = float('inf')
    else:
        psnr_value = 10 * np.log10((255**2) / mse_value)
    
    # Dice similarity coefficient (for binary images, less relevant for color images but included)
    # Convert to binary for dice calculation
    original_bw = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) > 127
    compared_bw = cv2.cvtColor(compared, cv2.COLOR_BGR2GRAY) > 127
    
    intersection = np.logical_and(original_bw, compared_bw).sum()
    dice_value = (2.0 * intersection) / (original_bw.sum() + compared_bw.sum())
    
    return {
        'SSIM': ssim_value,
        'MSE': mse_value,
        'PSNR': psnr_value,
        'Dice': dice_value
    }

if __name__ == "__main__":
    # Example usage
    metrics = calculate_metrics("processed_image.png", "decrypted_image.png")
    print(metrics)