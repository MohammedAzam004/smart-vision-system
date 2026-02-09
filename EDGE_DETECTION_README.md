# Edge Detection - Documentation

## Overview
Image processing application that applies Canny edge detection to convert images into edge-only representations. This script demonstrates fundamental computer vision concepts by extracting edges from images, which is essential for many advanced CV applications.

## Features
- Canny edge detection algorithm
- Dual threshold edge detection
- Grayscale conversion preprocessing
- Command-line image path support
- Side-by-side original and edge comparison

## Technical Details

### What is Edge Detection?

Edge detection identifies boundaries within images where brightness changes sharply. These boundaries typically represent:
- Object outlines
- Surface discontinuities
- Material changes
- Shadows and depth changes

### Canny Edge Detection Algorithm

Developed by John F. Canny in 1986, it's a multi-stage algorithm:

**Stage 1: Noise Reduction**
- Uses Gaussian filter to smooth image
- Reduces noise that could be mistaken for edges

**Stage 2: Gradient Calculation**
- Finds intensity gradients
- Determines edge strength and direction

**Stage 3: Non-Maximum Suppression**
- Thins edges to single-pixel width
- Removes pixels that aren't part of an edge

**Stage 4: Double Threshold**
- Classifies edges as strong, weak, or non-edges
- Uses two threshold values (100 and 200 in this code)

**Stage 5: Edge Tracking by Hysteresis**
- Keeps weak edges connected to strong edges
- Removes isolated weak edges

## Usage

### Basic Run (Interactive)
```bash
python edge_detect.py
```
If no image path provided, defaults to looking for `sample_image.png` in current directory.

### With Command Line Argument
```bash
python edge_detect.py path/to/your/image.jpg
```

### Supported Image Formats
- PNG
- JPG/JPEG
- BMP
- TIFF
- WebP
- Any format supported by OpenCV

## Code Breakdown

### 1. Import and Path Handling
```python
import cv2
import sys

image_path = sys.argv[1] if len(sys.argv) > 1 else "sample_image.png"
img = cv2.imread(image_path)
```
- Accepts image path from command line
- Falls back to default if no argument provided

### 2. Error Handling
```python
if img is None:
    print(f"Error: Could not load image from {image_path}")
    print("Usage: python edge_detect.py <image_path>")
    sys.exit(1)
```
Validates image loading before processing.

### 3. Grayscale Conversion
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
Converts BGR (OpenCV default) to grayscale for edge detection.

**Why grayscale?**
- Edges are about intensity changes, not color
- Simpler computation (1 channel vs 3)
- Better performance
- Standard practice for edge detection

### 4. Edge Detection
```python
edge = cv2.Canny(gray, 100, 200)
```

**Parameters:**
- `gray`: Input grayscale image
- `100`: Lower threshold for hysteresis
- `200`: Upper threshold for hysteresis

**Threshold Guidelines:**
- Ratio of 1:2 or 1:3 is recommended
- Lower values = more edges (including noise)
- Higher values = fewer, stronger edges

### 5. Display Results
```python
cv2.imshow("original", img)
cv2.imshow("edge", edge)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
Shows original and edge-detected images side by side.

## Parameter Tuning

### Sensitive Edge Detection (More Edges)
```python
edge = cv2.Canny(gray, 50, 100)
```
Lower thresholds detect more subtle edges.

### Conservative Edge Detection (Fewer Edges)
```python
edge = cv2.Canny(gray, 150, 300)
```
Higher thresholds detect only strong edges.

### Very Fine Details
```python
edge = cv2.Canny(gray, 30, 90)
```
Captures very fine details and textures.

### Only Major Edges
```python
edge = cv2.Canny(gray, 200, 400)
```
Captures only the most prominent edges.

## Advanced Preprocessing

### Reduce Noise Before Detection
```python
# Apply Gaussian blur first
blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
edge = cv2.Canny(blurred, 100, 200)
```

### Enhance Contrast
```python
# Histogram equalization
equalized = cv2.equalizeHist(gray)
edge = cv2.Canny(equalized, 100, 200)
```

### Adaptive Thresholding
```python
# Calculate automatic thresholds
median = np.median(gray)
lower = int(max(0, 0.7 * median))
upper = int(min(255, 1.3 * median))
edge = cv2.Canny(gray, lower, upper)
```

## Saving Output

### Save Edge Image
```python
cv2.imwrite("output_edges.png", edge)
```

### Save Side-by-Side Comparison
```python
combined = np.hstack([gray, edge])
cv2.imwrite("comparison.png", combined)
```

### Save with Different Formats
```python
cv2.imwrite("edges.jpg", edge, [cv2.IMWRITE_JPEG_QUALITY, 95])
cv2.imwrite("edges.png", edge, [cv2.IMWRITE_PNG_COMPRESSION, 9])
```

## Practical Applications

### 1. Object Detection Preprocessing
```python
# Find contours from edges
contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

### 2. Document Scanning
```python
# Enhance document edges
kernel = np.ones((3,3), np.uint8)
dilated = cv2.dilate(edge, kernel, iterations=1)
```

### 3. Lane Detection (for Autonomous Vehicles)
```python
# Apply region of interest
mask = np.zeros_like(edge)
cv2.fillPoly(mask, roi_vertices, 255)
masked_edges = cv2.bitwise_and(edge, mask)
```

### 4. Shape Detection
```python
# Approximate shapes from edges
approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
```

## Troubleshooting

### Too Many Edges (Noisy)
**Problem**: Image shows excessive edge noise

**Solutions:**
```python
# 1. Increase thresholds
edge = cv2.Canny(gray, 150, 300)

# 2. Add more blur
gray = cv2.GaussianBlur(gray, (7, 7), 2.0)
edge = cv2.Canny(gray, 100, 200)

# 3. Use bilateral filter (preserves edges while reducing noise)
filtered = cv2.bilateralFilter(gray, 9, 75, 75)
edge = cv2.Canny(filtered, 100, 200)
```

### Too Few Edges (Missing Details)
**Problem**: Important edges not detected

**Solutions:**
```python
# 1. Lower thresholds
edge = cv2.Canny(gray, 50, 100)

# 2. Enhance contrast first
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced = clahe.apply(gray)
edge = cv2.Canny(enhanced, 100, 200)

# 3. Reduce blur
gray = cv2.GaussianBlur(gray, (3, 3), 0.5)
edge = cv2.Canny(gray, 100, 200)
```

### Image Not Loading
**Check:**
1. File path is correct
2. File format supported
3. File not corrupted
4. Permissions to read file

```python
import os
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
```

## Code Flow

```
1. Check command line arguments
2. Set image path (from argument or default)
3. Load image using cv2.imread()
4. Validate image loaded successfully
5. Convert image to grayscale
6. Apply Canny edge detection
7. Display original image window
8. Display edge-detected image window
9. Wait for key press
10. Close all windows
```

## Performance Considerations

### Speed Optimizations
```python
# Process at lower resolution
scale = 0.5
small_img = cv2.resize(img, None, fx=scale, fy=scale)
gray = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray, 100, 200)
# Resize back if needed
edge = cv2.resize(edge, (img.shape[1], img.shape[0]))
```

### Typical Processing Times
- 640x480 image: ~5-10ms
- 1920x1080 image: ~20-40ms
- 4K image: ~80-150ms

## Real-World Example Use Cases

### Security & Surveillance
- Motion detection
- Intrusion detection
- Perimeter monitoring

### Medical Imaging
- Tumor boundary detection
- Organ segmentation
- X-ray analysis

### Manufacturing
- Quality control
- Defect detection
- Part inspection

### Robotics
- Object recognition
- Navigation
- Obstacle avoidance

### Photography
- Artistic effects
- Portrait mode preprocessing
- HDR edge-aware blending

## Comparison with Other Edge Detectors

### Sobel Edge Detection
```python
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
sobel = np.sqrt(sobelx**2 + sobely**2)
```
- Faster than Canny
- Less accurate
- Shows gradient magnitude

### Laplacian Edge Detection
```python
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```
- Single operation
- More sensitive to noise
- Detects edges in all directions simultaneously

### Why Canny is Better
- More accurate
- Better noise suppression
- Thinner edges
- Industry standard
- Highly reliable

## Requirements

- Python 3.8+
- OpenCV 4.0+
- NumPy
- Image file to process

## Batch Processing

Process multiple images:
```python
import glob

for img_path in glob.glob("images/*.jpg"):
    img = cv2.imread(img_path)
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 100, 200)
        output_path = img_path.replace(".jpg", "_edges.jpg")
        cv2.imwrite(output_path, edge)
        print(f"Processed: {img_path}")
```

## Video Processing

Apply to video frames:
```python
cap = cv2.VideoCapture("video.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 100, 200)
    cv2.imshow("Edges", edge)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

## Next Steps

- Combine with contour detection
- Implement Hough line detection
- Add shape recognition
- Create artistic effects
- Build document scanner
- Implement AR marker detection

## Best Practices

1. **Always convert to grayscale** before edge detection
2. **Preprocess to reduce noise** (blur, denoise)
3. **Tune thresholds** for your specific use case
4. **Consider image resolution** (resize if needed for speed)
5. **Combine with other techniques** for better results

## Resources

- [Canny Edge Detection Paper](https://ieeexplore.ieee.org/document/4767851)
- [OpenCV Edge Detection Tutorial](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [Image Gradients](https://docs.opencv.org/4.x/d5/d0f/tutorial_py_gradients.html)

## License
Open source - MIT License

## Note
Edge detection is a fundamental building block in computer vision. Master this technique as it's used in countless advanced CV applications.
