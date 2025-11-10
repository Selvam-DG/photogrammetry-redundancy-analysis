#  ReduVis — Redundancy & Similarity Analysis for Photogrammetry Datasets

### Optimized Preprocessing Stage for Meshroom / COLMAP Pipelines

ReduVis intelligently detects and removes redundant or near-duplicate images from preprocessed datasets (e.g., output from [VisionPrep](../VisionPrep)).

---

##  Key Features

- Perceptual + structural similarity (pHash, dHash, SSIM)
- DBSCAN or KMeans clustering for redundancy grouping
- Automatically keeps the sharpest image per cluster
- Generates reports, heatmaps, and performance metrics
- 100% CPU-based — works on low-end laptops

---

##  Example Workflow

```bash
python reduvis.py --input "C:/VisionPrep/output"
```
**Output**
```bash
outputs/
├── kept/       # Optimized dataset for photogrammetry
├── removed/    # Discarded redundant images
└── reports/
    ├── heatmap.png
    ├── reduvis_report_*.csv
    └── summary.json
```

## Why It Matters
| Problem                               | ReduVis Solution                              |
| ------------------------------------- | --------------------------------------------- |
| Large datasets with overlapping views | Groups similar images via perceptual distance |
| Long SfM/MVS runtimes                 | Keeps only representative frames              |
| Low hardware resources                | Lightweight CPU processing                    |

## Example Results
| Metric                 | Before       | After |
| ---------------------- | ------------ | ----- |
| Images                 | 200          | 120   |
| SfM Time               | 100%         | ~55%  |
| Feature Density        | 100%         | 96%   |
| Reconstruction Quality | ✓ Maintained |       |

## Configurable Parameters

| Parameter             | Description                | Default  |
| --------------------- | -------------------------- | -------- |
| `resize_max`          | Resize for speed           | 800      |
| `hash_size`           | Hash grid size             | 16       |
| `clustering.eps`      | DBSCAN radius              | 0.18     |
| `selection.criterion` | Keep sharpest or brightest | sharpest |

## Evaluation Metrics

- Sharpness (Laplacian Variance)
- Brightness Mean
- SSIM Similarity
- Feature Loss %
- Estimated Speed Gain %

## Ideal Pipeline Integration
```
Videos → Raw Images → image_preprocessing → Similarity Analysis → Meshroom / COLMAP → 3D Model
```
## Future Enhancements

- Adaptive parameter tuning using feature density feedback
- Integration into a unified GUI pipeline
- Lightweight model for image uniqueness prediction (CNN-based)


## License

* MIT License © 2025 
* Developed for  Photogrammetry Optimization