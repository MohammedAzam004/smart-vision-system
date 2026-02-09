# Number Plate Detection - Documentation

## Overview
Real-time vehicle license plate detection system using OpenCV and Haar Cascade classifiers. This script captures video from your webcam and automatically detects and highlights vehicle number plates with bounding boxes and labels.

## Features
- Real-time license plate detection
- Green bounding boxes around detected plates
- Text labels for identification
- Adjustable detection sensitivity
- Works with Russian plate format (adaptable to other formats)

## Technical Details

### Algorithm: Haar Cascade Classifier for Plates

**Cascade Classifier Loading**
```python
plate_cascade = cv2.CascadeClassifier("models/haarcascade_russian_plate_number.xml")
```

This specialized Haar Cascade is trained specifically to recognize the patterns and characteristics of Russian-style license plates.

### Detection Process

**1. Grayscale Conversion**
```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
Converts color image to grayscale for better pattern recognition.

**2. Plate Detection**
```python
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
```

**Parameters:**
- `scaleFactor=1.1`: Image pyramid scale reduction
  - Lower = more thorough scanning
  - Higher = faster but may miss plates
- `minNeighbors=10`: Required neighbor rectangles
  - Higher = fewer false positives
  - Lower = more detections (but more noise)

**3. Visual Feedback**
```python
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
cv2.putText(frame, "Number Plate", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
```
- Green rectangle outlines the plate
- "Number Plate" label above detection

## Usage

### Basic Run
```bash
python number_plate_detec.py
```

### Controls
- **Press 'q'**: Exit the application
- **ESC**: Alternative exit method

### Best Practices
1. **Position plate clearly** in camera view
2. **Good lighting** - avoid shadows and glare
3. **Proper distance** - plate should be visible but not too small
4. **Minimal motion** - slower movement improves detection
5. **Clean plates** - dirt or damage may affect detection

## Parameter Tuning

### More Sensitive Detection
```python
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
```
- Detects more plates
- More false positives
- Slower processing

### More Accurate Detection
```python
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=15)
```
- Fewer false positives
- May miss some plates
- Faster processing

### Add Size Constraints
```python
plates = plate_cascade.detectMultiScale(
    gray, 
    scaleFactor=1.1, 
    minNeighbors=10,
    minSize=(50, 20),  # Minimum plate size
    maxSize=(400, 200)  # Maximum plate size
)
```
Helps filter out incorrect detections.

## Code Flow

```
1. Load Haar Cascade classifier for plates
2. Initialize video capture (webcam)
3. Loop continuously:
   a. Read frame from camera
   b. Check if frame captured successfully
   c. Convert frame to grayscale
   d. Detect number plates
   e. For each detected plate:
      - Draw green rectangle
      - Add "Number Plate" label
   f. Display result window
   g. Check for 'q' key press
4. Release camera and close windows
```

## Troubleshooting

### No Plates Detected

**Possible Causes:**
- Model file not found or corrupted
- Plate format doesn't match trained model
- Poor lighting conditions
- Plate too small or too far
- Plate at extreme angle

**Solutions:**
```python
# 1. Verify model file exists
import os
if not os.path.exists("models/haarcascade_russian_plate_number.xml"):
    print("Model file missing!")

# 2. Reduce minNeighbors
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# 3. Improve lighting
# Use external lights or adjust camera exposure

# 4. Zoom in or move closer
# Ensure plate takes up reasonable portion of frame
```

### Too Many False Positives

**Problem**: Detecting non-plate objects

**Solutions:**
```python
# 1. Increase minNeighbors
plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=15)

# 2. Add size constraints
plates = plate_cascade.detectMultiScale(
    gray, 
    scaleFactor=1.1, 
    minNeighbors=10,
    minSize=(100, 40),
    maxSize=(300, 150)
)

# 3. Filter by aspect ratio
for (x, y, w, h) in plates:
    aspect_ratio = w / h
    if 2.0 < aspect_ratio < 5.0:  # Typical plate ratio
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
```

### Camera Not Opening

**Check:**
1. Camera is connected
2. No other application using camera
3. Camera permissions granted
4. Try different camera index:
```python
cap = cv2.VideoCapture(1)  # or 2, 3, etc.
```

### Poor Detection Accuracy

**Improve accuracy:**
```python
# Enhance image preprocessing
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)  # Enhance contrast
gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
```

## Advanced Features

### Add Plate Counting
```python
plate_count = 0
for (x, y, w, h) in plates:
    plate_count += 1
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.putText(frame, f"Plate #{plate_count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
```

### Save Detected Plates
```python
for i, (x, y, w, h) in enumerate(plates):
    plate_img = frame[y:y+h, x:x+w]
    cv2.imwrite(f"plate_{i}_{time.time()}.jpg", plate_img)
```

### Add Timestamp
```python
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
```

### Log Detection Events
```python
if len(plates) > 0:
    with open("detections.log", "a") as log:
        log.write(f"{datetime.now()}: {len(plates)} plate(s) detected\n")
```

## Extending to Other Plate Formats

### Using Different Models

**European Plates:**
```python
plate_cascade = cv2.CascadeClassifier("models/haarcascade_european_plate.xml")
```

**Indian Plates:**
```python
plate_cascade = cv2.CascadeClassifier("models/haarcascade_indian_plate.xml")
```

### Training Custom Cascade

For plates in your region:
1. Collect positive samples (plates)
2. Collect negative samples (non-plates)
3. Use OpenCV's `opencv_traincascade` tool
4. Generate your own XML file

Resources:
- [Cascade Training Tutorial](https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html)

## Integration with OCR

For reading plate numbers, integrate with OCR:

```python
import pytesseract

for (x, y, w, h) in plates:
    plate_img = gray[y:y+h, x:x+w]
    # Enhance for OCR
    plate_img = cv2.threshold(plate_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(plate_img, config='--psm 7')
    print(f"Plate Number: {text}")
```

## Requirements

- Python 3.8+
- OpenCV 4.0+
- Webcam or video source
- Model file: `haarcascade_russian_plate_number.xml`

## Model File

Download from OpenCV's GitHub repository:
[haarcascade_russian_plate_number.xml](https://github.com/opencv/opencv/tree/master/data/haarcascades)

Place in `models/` directory.

## Performance

### Speed
- **Modern CPU**: 25-40 FPS
- **Older Hardware**: 15-25 FPS
- **With enhancement**: 10-20 FPS

### Accuracy
- **Good lighting**: 80-90% detection rate
- **Poor lighting**: 40-60% detection rate
- **Optimal angle**: Near frontal view
- **Range**: Works best at 2-10 meters

## Use Cases

### Parking Management
- Automated entry/exit logging
- Parking space allocation
- Payment systems

### Security & Surveillance
- Vehicle tracking
- Access control
- Security alerts

### Traffic Monitoring
- Speed enforcement preprocessing
- Traffic flow analysis
- Vehicle counting

### Law Enforcement
- Wanted vehicle detection
- Stolen vehicle identification
- Evidence collection

## Limitations

- **Angle sensitivity**: Best with frontal or near-frontal views
- **Lighting dependent**: Poor performance in low light
- **Format specific**: Trained for specific plate formats
- **False positives**: May detect similar rectangular objects
- **Motion blur**: Fast-moving vehicles harder to detect
- **Occlusion**: Dirty, damaged, or partially hidden plates

## Legal & Privacy Considerations

**Important:**
- Check local laws regarding automated plate reading
- Obtain proper authorization for surveillance
- Respect privacy regulations (GDPR, etc.)
- Secure storage of plate data
- Clear data retention policies

## Optimization Tips

### For Better Accuracy
1. Use high-resolution camera
2. Ensure proper lighting
3. Position camera at optimal angle
4. Regular model updates
5. Combine with other detection methods

### For Better Performance
1. Reduce frame resolution
2. Process every Nth frame
3. Use GPU acceleration (if available)
4. Optimize cascade parameters
5. Multi-threading for detection

## Next Steps

- Add OCR for plate number extraction
- Implement plate tracking across frames
- Create database of detected plates
- Add cloud storage integration
- Implement real-time alerts
- Multi-camera support
- Machine learning-based detection

## Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [YOLO for Plate Detection](https://github.com/quangnhat185/Plate_detect_and_recognize)
- [Automatic Number Plate Recognition](https://github.com/topics/anpr)

## License
Open source - MIT License

## Disclaimer
This tool is for educational and authorized use only. Ensure compliance with local laws and regulations regarding automated vehicle monitoring and data privacy.
