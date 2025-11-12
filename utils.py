import os, cv2, json, shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def ensure_dirs(paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def load_images_from_folder(folder, resize_max):
    images = []
    names = []
    for file in sorted(os.listdir(folder)):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            path = os.path.join(folder, file)
            img = cv2.imread(path)
            h,w = img.shape[:2]
            scale = resize_max / max(h, w)
            if scale < 1.0:
                img = cv2.resize(img, (int(w*scale), int(h*scale)))
            images.append(img)
            names.append(file)
    return images, names

def plot_heatmap(matrix, names, save_path):
    plt.figure(figsize=(10,8))
    sns.heatmap(matrix, cmap="viridis")
    plt.title("Image Similarity Heatmap")
    plt.savefig(save_path)
    plt.close()
    
def log_results(data, output_dir):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = os.path.join(output_dir, f"reduvis_report_{ts}.csv")
    pd.DataFrame(data).to_csv(csv_path, index=False)
    return csv_path
        