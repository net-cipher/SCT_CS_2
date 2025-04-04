import cv2
import numpy as np
from random import shuffle
import os

def swap_pixels(image_path, key):
    if not os.path.exists(image_path):
        raise ValueError("Image not found, check file path")
    
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or unable to read")
    
    height, width, _ = image.shape
    indices = [(i, j) for i in range(height) for j in range(width)]
    shuffled_indices = indices.copy()
    shuffle(shuffled_indices)
    
    encrypted_image = np.zeros_like(image)
    for (orig, shuffled) in zip(indices, shuffled_indices):
        encrypted_image[shuffled] = image[orig]
    
    encrypted_path = os.path.splitext(image_path)[0] + "_encrypted_swap.jpg"
    cv2.imwrite(encrypted_path, encrypted_image)
    
    return encrypted_path, shuffled_indices

def reverse_swap(image_path, shuffled_indices):
    if not os.path.exists(image_path):
        raise ValueError("Encrypted image file not found. Check the file path.")
    
    encrypted_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if encrypted_image is None:
        raise ValueError("Encrypted image not found or unable to read")
    
    height, width, _ = encrypted_image.shape
    decrypted_image = np.zeros_like(encrypted_image)
    indices = [(i, j) for i in range(height) for j in range(width)]
    
    for (orig, shuffled) in zip(indices, shuffled_indices):
        decrypted_image[orig] = encrypted_image[shuffled]
    
    decrypted_path = os.path.splitext(image_path)[0] + "_decrypted_swap.jpg"
    cv2.imwrite(decrypted_path, decrypted_image)
    
    return decrypted_path

def apply_math_operation(image_path, key):
    if not os.path.exists(image_path):
        raise ValueError("Image file not found. Check the file path.")
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image not found or unable to read")
    encrypted_image = np.clip(image.astype(np.int16) + key, 0, 255).astype(np.uint8)
    encrypted_path = os.path.splitext(image_path)[0] + "_encrypted_math.jpg"
    cv2.imwrite(encrypted_path, encrypted_image)
    return encrypted_path

def reverse_math_operation(image_path, key):
    if not os.path.exists(image_path):
        raise ValueError("Encrypted image file not found. Check the file path.")
    encrypted_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if encrypted_image is None:
        raise ValueError("Encrypted image not found or unable to read")
    decrypted_image = np.clip(encrypted_image.astype(np.int16) - key, 0, 255).astype(np.uint8)
    decrypted_path = os.path.splitext(image_path)[0] + "_decrypted_math.jpg"
    cv2.imwrite(decrypted_path, decrypted_image)
    return decrypted_path
if __name__ == "__main__":
    image_path = input("Enter the image file path: ")
    key = int(input("Enter the encryption key (integer): "))

    try:
        encrypted_path, indices = swap_pixels(image_path, key)
        print(f"Encrypted Swap sved at: {encrypted_path}")
        decrypted_path = reverse_swap(encrypted_path, indices)
        print(f"Decrypted and saved in {decrypted_path}")
        # Math oper
        encrypted_math_path = apply_math_operation(image_path, key)
        print(f"Encrypted Math Image saved at: {encrypted_math_path}")
        decrypted_math_path = reverse_math_operation(encrypted_math_path, key)
        print(f"Decrypted Math Image saved at: {decrypted_math_path}")
    except ValueError as e:
        print(f"Error: {e}")
