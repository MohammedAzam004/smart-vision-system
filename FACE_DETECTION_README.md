# Face Detection - Documentation

## Overview
Real-time face detection application using OpenCV's Haar Cascade Classifier. This script captures video from your webcam and detects human faces in real-time, drawing rectangular bounding boxes around them.

## Features
- Real-time face detection from webcam feed
- Adjustable detection sensitivity
- Visual feedback with bounding boxes
- Low latency performance

## Technical Details

### Algorithm: Haar Cascade Classifier
The Haar Cascade Classifier is a machine learning-based approach for object detection:
- Uses Haar-like features to detect patterns
- Trained on thousands of positive and negative images
- Fast and efficient for real-time applications

### Key Components

**1. Cascade Classifier Loading**
```python
face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
```
Loads the pre-trained Haar Cascade model for frontal face detection.

**2. Video Capture**
```python
cap = cv2.VideoCapture(0)
```
- `0` represents the default camera
- Change to `1` or `2` if you have multiple cameras

**3. Grayscale Conversion**
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
Converts BGR image to grayscale for better detection performance.

**4. Face Detection**
```python
detect_face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
```

**Parameters:**
- `scaleFactor=1.1`: Image pyramid scale reduction (1.1 = 10% reduction per layer)
- `minNeighbors=3`: Minimum number of neighbor rectangles to retain detection
  - Lower values = more detections (but more false positives)
  - Higher values = fewer detections (but more accurate)

**5. Drawing Rectangles**
```python
cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 125, 100), 3) ```

**Parameters:**
- `(x, y)`: Top-left corner coordinates
- `(x+w, y+h)`: Bottom-right corner coordinates
- `(50, 125, 100)`: BGR color values
- `3`: Rectangle thickness in pixels

## Usage

### Basic Run
```bash
python face_detection.py
```

### Controls
- **Press 'q'**: Quit the application
- **ESC**: Alternative exit method

## Performance Tuning

### Improve Detection Accuracy
Increase `minNeighbors`:
```python
detect_face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
```

### Improve Detection Speed
Increase `scaleFactor`:
```python
detect_face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)
```

### Adjust Detection Range
Add `minSize` and `maxSize`:
```python
detect_face = face_cascade.detectMultiScale(
    gray, 
    scaleFactor=1.1, 
    minNeighbors=3,
    minSize=(30, 30),
    maxSize=(300, 300)
)
```

## Troubleshooting

### No Faces Detected
- Ensure proper lighting
- Face the camera directly
- Reduce `minNeighbors` value
- Check camera is working

### Too Many False Positives
- Increase `minNeighbors` value
- Increase `scaleFactor`
- Add minimum size constraints

### Camera Not Opening
- Verify camera is connected
- Try changing camera index to `1` or `2`
- Check camera permissions

## Code Flow

```
1. Load Haar Cascade classifier
2. Initialize video capture
3. Loop continuously:
   a. Read frame from camera
   b. Convert to grayscale
   c. Detect faces
   d. Draw rectangles around faces
   e. Display result
   f. Check for 'q' key press
4. Release resources and close windows
```

## Requirements
- Python 3.8+
- OpenCV 4.0+
- Webcam
- Haar Cascade XML file in `models/` directory

## Model Files Required
- `haarcascade_frontalface_default.xml`

Download from: [OpenCV Haarcascades](https://github.com/opencv/opencv/tree/master/data/haarcascades)

## Use Cases
- Attendance systems
- Security surveillance previews
- Face detection preprocessing
- Learning computer vision basics
- Real-time face tracking

## Limitations
- Works best with frontal faces
- Requires good lighting
- May not detect faces at extreme angles
- Not suitable for face recognition (only detection)

## Next Steps
- Combine with face recognition
- Add face counting
- Implement face blur/anonymization
- Add gender/age estimation
- Track faces across frames

## License
Open source - MIT License
