import numpy as np
from sklearn.cluster import DBSCAN, KMeans

def cluster_features(distance_matrix, method='dbscan', eps=0.18, min_samples=2, k=None):
    """
    Clusters images based on pairwise distance matrix.
    """
    if method == "dbscan":
        model = DBSCAN(metric="precomputed", eps=eps, min_samples=min_samples)
        labels = model.fit_predict(distance_matrix)
    elif method == 'kmeans':
        if k is None:
            k = int(np.sqrt(len(distance_matrix) / 2))
        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(distance_matrix)
        
    else:
        raise ValueError("Unsupported clustering method.")
    
    return labels