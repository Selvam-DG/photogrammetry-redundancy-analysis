import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compute_phash(image, hash_size=16):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size+1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return diff.flatten().astype(int)

def compute_dhash(image, hash_size=16):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size+1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return diff.flatten().astype(int)

def hamming_distance(hash1, hash2):
    return np.sum(hash1 != hash2) / len(hash1)

def compute_ssim(img1, img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    s, _ = ssim(gray_img1, gray_img2, full=True)
    return s

def laplacian_variance(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

    