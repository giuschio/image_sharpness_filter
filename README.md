# Vision Utils

## Offline sharpness filter
**Commandline usage:**  
```bash
python3 src/offline_sharpness_filter.py abs/input_path abs/output_path --downsampling_factor 10 --sharpness_threshold 30
```

**Metrics:**
- sharpness of an image is measured as the variance of Laplacian kernel (higher is better)

**Assumptions:**
- images are sequential

**Working principle:**
- calculate image sharpness for all images in the `input_dir`
- calculate minimum absolute sharpness:
    ```python
    min_sharpness = percentile(distribution=images_sharpness, percentile=sharpness_threshold
    ```
- slide a sliding window of dimension `downsampling_factor` over the image list. Keep an image if it is the sharpest in its window `AND` it is sharper than the `min_sharpness`

