# ReduVis Features

## Overview
ReduVis is an interactive web application for identifying and removing redundant images in photogrammetry datasets. Built with Streamlit, it provides a visual interface for redundancy analysis.

## Core Features

### Image Processing
- **Multi-metric similarity detection**: Combines perceptual hashing (pHash), difference hashing (dHash), and structural similarity (SSIM)
- **DBSCAN clustering**: Groups redundant images automatically
- **Quality-based selection**: Retains sharpest image from each cluster using Laplacian variance
- **Configurable parameters**: Adjustable weights and thresholds via YAML configuration

### User Interface
- **ZIP folder upload**: Direct upload of preprocessed image collections
- **Interactive visualization**: Real-time similarity heatmap display
- **Summary statistics**: Total, kept, removed images with reduction percentage
- **Progress tracking**: Visual feedback during processing

### Output & Export
- **Optimized image set**: Download deduplicated images as `kept_images.zip`
- **Detailed CSV report**: Image-level metrics including cluster assignments and sharpness scores
- **Preserved archives**: Removed images saved separately for review

## Use Cases
- Pre-processing for photogrammetry reconstruction
- Dataset optimization for 3D modeling pipelines
- Video frame deduplication
- Computer vision dataset curation

## Technical Details
- Python-based with OpenCV, NumPy, scikit-learn
- Streamlit web framework
- Modular architecture with separated core logic
- YAML-based configuration system

---

*For setup and usage instructions, see README.md*