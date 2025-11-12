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
    
    ensure_dirs(cfg['output_dirs'].values())
    
    images, names = load_images_from_folder(input_dir, cfg['resize_max'])
    n = len(images)
    print(f"[INFO] Loaded {n} images from {input_dir}")
    
    p_hashes = [compute_phash(img, cfg['hash_size']) for img in images]
    d_hashes = [compute_dhash(img, cfg['hash_size']) for img  in images]
    
    print(f"[INFO] Computing Similarity matrix....")
    dist_matrix = np.zeros((n,n))
    
    for i in tqdm(range(n)):
        for j in range(i+1, n):
            dist_phash = hamming_distance(p_hashes[i], p_hashes[j])
            dist_dhash = hamming_distance(d_hashes[i], d_hashes[j])
            s_ssim = 1 - compute_ssim(images[i], images[j])
            dist = (cfg['weights']['phash'] * dist_phash + cfg['weights']['dhash'] * dist_dhash + cfg['weights']['ssim'] * s_ssim )
            dist_matrix[i,j] = dist_matrix[j, i] = dist
            
            
    labels = cluster_features(dist_matrix, method=cfg['clustering']['method'], eps=cfg['clustering']['eps'],
                              min_samples=cfg['clustering']['min_samples'])
    
    print(f"[INFO] Selecting reperesentative images....")
    
    cluster_map= {}
    report = []
    for idx, label in enumerate(labels):
        cluster_map.setdefault(label, []).append(idx)
    
    kept, removed = [], []
    for label, indices in cluster_map.items():
        if label == -1:
            kept.extend(indices)
            continue
        sharpness = [laplacian_variance(images[i]) for i in indices]
        keep_idx = indices[np.argmax(sharpness)]
        kept.append(keep_idx)
        for i in indices:
            if i != keep_idx:
                removed.append(i)
    for i in kept:
        cv2.imwrite(os.path.join(cfg['output_dirs']['kept'], names[i]), images[i])
    for i in removed:
        cv2.imwrite(os.path.join(cfg['output_dirs']['removed'], names[i]), images[i])
    
    plot_heatmap(dist_matrix, names, os.path.join(cfg['output_dirs']['report'], "heatmap.png"))
    
    summary = {
        "total_images": n,
        "kept" : len(kept),
        "removed" : len(removed),
        "removed_percentage" : round(100 * len(removed)/n, 2),
        "runtime_sec" : round(time.time() - start_time, 2)          
    }
    print(f"[Summary] {summary}")
    
    csv_path = log_results([
        {'name': names[i], 
         "cluster": int(labels[i]),
         "kept" : i in kept,
         "sharpness" : laplacian_variance(images[i])
         } for i in range(n)
    ], cfg['output_dirs']['report'])
    
    with open(os.path.join(cfg['output_dirs']['report'], "summary.jsoon"), "w") as f:
        import json
        json.dump(summary, f, indent=4)
    print(f"[INFO] Report saved to {csv_path}")
    
    return summary

if __name__ == "__main__":
    input_dir = r"D:\Think3DDD\mini_projects\1_smart_image_preprocessing_VisionPrep\output"
    run_reduvis(input_dir)
    
