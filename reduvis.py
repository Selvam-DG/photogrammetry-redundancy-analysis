import os, yaml, cv2, time
import numpy as np
from tqdm import tqdm
from similarity_metrics import compute_phash, compute_dhash, hamming_distance, compute_ssim, laplacian_variance
from clustering import cluster_features
from utils import ensure_dirs, load_images_from_folder, plot_heatmap, log_results

def run_reduvis(input_dir, config_path="config.yaml"):
    start_time = time.time()
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
    
    ensure_dirs(cfg['output_dirs'])
