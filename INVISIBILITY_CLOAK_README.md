# Invisibility Cloak - Documentation

## Overview
A Harry Potter-inspired invisibility cloak effect that makes objects of a specific color appear transparent by replacing them with a pre-captured background. Supports **5 colors**: Red, Blue, Green, Yellow, and Black. Choose your preferred color for the ultimate invisibility experience!

## Features
- **5 Color Options**: Red, Blue, Green, Yellow, Black
- Interactive color selection menu
- Real-time invisibility effect
- Adjustable color detection
- Smooth edge processing
- Video recording capability
- Mirror-like display for user convenience

## Color Selection

### Available Colors & HSV Ranges

| Color | Hue Range | Best Use Case |
|-------|-----------|---------------|
| **🔴 Red** | 0-10, 170-180 | Indoor settings, most versatile |
| **🔵 Blue** | 100-140 | Outdoor, well-lit environments |
| **🟢 Green** | 40-80 | Indoor, contrasts well with most backgrounds |
| **🟡 Yellow** | 20-30 | Bright lighting, high visibility |
| **⚫ Black** | All hues, low brightness | Low-light conditions |

### How to Select Color

**Standalone Script:**
```bash
python invisibility_clock.py
```
You'll see an interactive menu:
```
==================================================
    INVISIBILITY CLOAK - COLOR SELECTION
==================================================

Select the color of your cloak:
  1. Red
  2. Blue
  3. Green
  4. Yellow
  5. Black
==================================================

Enter your choice (1-5): 
```

**Streamlit Web App:**
1. Navigate to "Invisibility Cloak" in sidebar
2. Use the dropdown menu: "🎨 Select Cloak Color"
3. Choose from: 🔴 Red, 🔵 Blue, 🟢 Green, 🟡 Yellow, ⚫ Black
4. Click "🚀 Start Cloak"

## How It Works

### Step-by-Step Process

**1. Background Capture (First 2 seconds)**
```python
time.sleep(2)
for i in range(20):
    ret, background = cap.read()
background = np.flip(background, axis=1)
```
- Captures stable background for 20 frames
- Mirrors the background to match live feed
- **Important:** Step out of frame during this phase!

**2. Color Space Conversion**
```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```
Converts from BGR to HSV color space:
- **Hue (H)**: Color type (0-180)
- **Saturation (S)**: Color intensity (0-255)
- **Value (V)**: Brightness (0-255)

**Why HSV?** Easier to isolate specific colors compared to RGB/BGR.

**3. Color Detection (Black by Default)**
```python
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])
mask = cv2.inRange(hsv, lower_black, upper_black)
```
Creates a binary mask:
- White (255) = pixels within color range (detected cloak)
- Black (0) = pixels outside range

**4. Mask Refinement**
```python
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)
```
- **MORPH_OPEN**: Removes small noise/holes
- **MORPH_DILATE**: Expands detected regions

**5. Create Inverse Mask**
```python
mask_inv = cv2.bitwise_not(mask)
```
Inverts the mask for non-cloak regions.

**6. Combine Images**
```python
result_1 = cv2.bitwise_and(background, background, mask=mask)
result_2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
final_output = cv2.addWeighted(result_1, 1, result_2, 1, 0)
```
- `result_1`: Background where cloak is detected
- `result_2`: Current frame where cloak is NOT detected
- Final: Seamless combination

## Usage

### Basic Run
```bash
python invisibility_clock.py
```

### Instructions
1. Run the script
2. **Select your preferred color** (1-5)
3. **Step away from the camera for 2 seconds** (background capture)
4. Hold a cloth matching your selected color in front of you
5. Watch it become invisible!
6. Press 'q' to exit

### Streamlit Web App
1. Open the app: `streamlit run app.py`
2. Select "Invisibility Cloak" from sidebar
3. Choose your color from the dropdown
4. Click "🚀 Start Cloak"
5. Step away during background capture
6. Hold your colored cloth and enjoy!
7. Click "⏹️ Stop Cloak" when done

### Output
- **Live Display**: Real-time window showing the effect
- **Window Title**: Shows selected color (e.g., "Invisibility Cloak - Blue")
- **Saved Video**: `invisibility_clock.avi` (20 FPS, 640x480)

## Built-in Color Options

### 1. 🔴 Red Cloak
**HSV Range:**
```python
Lower1: [0, 120, 70]    → [10, 255, 255]
Lower2: [170, 120, 70]  → [180, 255, 255]
```
**Best For:** Indoor environments, general use  
**Note:** Red wraps around HSV hue scale (requires two ranges)

### 2. 🔵 Blue Cloak  
**HSV Range:**
```python
Lower: [100, 150, 50]   → [140, 255, 255]
```
**Best For:** Outdoor settings, bright lighting  
**Note:** Excellent color separation from skin tones

### 3. 🟢 Green Cloak
**HSV Range:**
```python
Lower: [40, 50, 50]     → [80, 255, 255]
```
**Best For:** Indoor use, chroma-key style effects  
**Note:** Popular for video production (green screen)

### 4. 🟡 Yellow Cloak
**HSV Range:**
```python
Lower: [20, 100, 100]   → [30, 255, 255]
```
**Best For:** Bright, well-lit environments  
**Note:** High visibility color, easy to detect

### 5. ⚫ Black Cloak
**HSV Range:**
```python
Lower: [0, 0, 0]        → [180, 255, 50]
```
**Best For:** Low-light conditions, dark backgrounds  
**Note:** Detects objects with very low brightness values

## Color Customization

### Adjusting Existing Colors in Code

To fine-tune a color's HSV range, edit the `COLORS` dictionary in `invisibility_clock.py`:

```python
COLORS = {
    '1': {
        'name': 'Red',
        'lower1': np.array([0, 120, 70]),      # Adjust these values
        'upper1': np.array([10, 255, 255]),    # for your lighting
        'lower2': np.array([170, 120, 70]),
        'upper2': np.array([180, 255, 255]),
        'has_two_ranges': True
    },
    # ... other colors
}
```

### Adding Custom Colors

Add a new color to the dictionary:

```python
'6': {
    'name': 'Purple',
    'lower1': np.array([130, 50, 50]),
    'upper1': np.array([160, 255, 255]),
    'has_two_ranges': False
}
```

### HSV Value Guide

- **Hue (H)**: Color type
  - Red: 0-10, 170-180
  - Yellow: 20-30
  - Green: 40-80
  - Blue: 100-140
  - Purple: 130-160

- **Saturation (S)**: Color intensity
  - Low (50-100): Pastel, washed out
  - Medium (100-200): Normal colors
  - High (200-255): Vivid, saturated

- **Value (V)**: Brightness
  - Low (0-50): Dark colors
  - Medium (50-150): Normal brightness
  - High (150-255): Bright colors

## Parameters Explained

### Video Settings
```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')
save_file = cv2.VideoWriter("invisibility_clock.avi", fourcc, 20.0, (640,480))
```
- **XVID**: Codec for compression
- **20.0**: Frames per second
- **(640, 480)**: Resolution

### Morphological Kernel
```python
kernel = np.ones((3,3), np.uint8)
```
- 3x3 matrix for morphological operations
- Larger kernel = more aggressive smoothing

## Tips for Best Results

### 1. Background Setup
- Use a **static, stable background**
- Avoid moving objects during capture
- Ensure good, even lighting
- Keep consistent distance from camera

### 2. Cloak Material
- Use **solid-colored** fabric matching your selection
- Avoid shiny/reflective materials
- Larger cloth = better coverage
- Hold cloth smoothly without wrinkles

### 3. Environment
- **Good lighting** is crucial
- Avoid shadows on the cloth
- Position yourself properly in frame
- Minimize background motion

### 4. Color Selection Guide

**🔴 Red** 
- ✅ Best all-around choice
- ✅ Works in most lighting
- ✅ Easy to find red fabric
- ⚠️ Avoid if wearing red clothes

**🔵 Blue**
- ✅ Excellent for outdoors
- ✅ Good contrast with skin
- ✅ Professional looking
- ⚠️ Requires brighter lighting

**🟢 Green**
- ✅ Classic chroma-key color
- ✅ Professional video effects
- ✅ Clear color separation
- ⚠️ Avoid green in background

**🟡 Yellow**
- ✅ Highly visible
- ✅ Fun and vibrant
- ✅ Quick detection
- ⚠️ Needs strong lighting

**⚫ Black**
- ✅ Works in low light
- ✅ Common fabric color
- ✅ Mysterious effect
- ⚠️ May detect shadows/dark areas

### 5. Lighting Conditions

| Color | Lighting Needed | Best Time |
|-------|----------------|-----------|
| Red | Moderate | Anytime |
| Blue | Bright | Daytime |
| Green | Moderate-Bright | Indoor/Outdoor |
| Yellow | Bright | Daytime |
| Black | Low-Moderate | Evening |

## Troubleshooting

### Cloak Not Detected

**General Solutions:**
- Check if cloth color matches selected option
- Improve lighting conditions
- Ensure cloth is fully visible to camera
- Try a different color option

**Color-Specific Issues:**

**Red Not Detected:**
```python
# Widen the HSV range
'lower1': np.array([0, 100, 60]),    # Lower saturation/value threshold
'upper1': np.array([15, 255, 255]),  # Slightly wider hue range
```

**Blue Not Detected:**
```python
# Adjust for darker blues
'lower1': np.array([95, 120, 40]),   # Capture darker shades
'upper1': np.array([145, 255, 255]),
```

**Green Not Detected:**
```python
# Capture more green variations
'lower1': np.array([35, 40, 40]),
'upper1': np.array([85, 255, 255]),
```

**Yellow Not Detected:**
```python
# Widen yellow range
'lower1': np.array([18, 80, 80]),
'upper1': np.array([32, 255, 255]),
```

**Black Not Detected:**
```python
# Increase brightness threshold for dark grays
'upper1': np.array([180, 255, 70]),  # Higher value threshold
```

### Background Showing Through Non-Cloak Areas
- Reduce detection range (narrow HSV values)
- Increase morphological iterations
- Use solid-colored background

### Jittery/Unstable Effect
- Increase MORPH_OPEN iterations
- Capture more background frames
- Use better quality webcam
- Stabilize camera position

### Performance Issues
- Reduce video resolution
- Lower FPS
- Optimize morphological operations
- Close other applications

## Technical Concepts

### Color Spaces
- **BGR**: Blue-Green-Red (OpenCV default)
- **RGB**: Red-Green-Blue (standard)
- **HSV**: Hue-Saturation-Value (best for color detection)

### Bitwise Operations
- **AND**: Keeps pixels where mask is white
- **OR**: Combines images
- **NOT**: Inverts mask
- **XOR**: Exclusive OR

### Morphological Operations
- **Erosion**: Shrinks white regions
- **Dilation**: Expands white regions
- **Opening**: Erosion followed by dilation (removes noise)
- **Closing**: Dilation followed by erosion (fills gaps)

## Code Flow

```
1. Initialize camera and video writer
2. Wait 2 seconds for camera warmup
3. Capture background (20 frames)
4. Mirror background horizontally
5. Loop continuously:
   a. Read current frame
   b. Mirror frame
   c. Convert to HSV
   d. Create color mask (detect cloak)
   e. Refine mask (morphology)
   f. Create inverse mask
   g. Extract background where cloak is
   h. Extract current frame where cloak isn't
   i. Combine both results
   j. Display and save output
   k. Check for 'q' key
6. Release resources
```

## Requirements
- Python 3.8+
- OpenCV 4.0+ (with GUI support)
- NumPy
- Webcam
- Colored cloth/fabric

## Video Output
- **Format**: AVI
- **Codec**: XVID
- **FPS**: 20
- **Resolution**: 640x480
- **Location**: Same directory as script

## Use Cases
- Entertainment and magic tricks
- Computer vision education
- Augmented reality demos
- Video effects and editing
- Understanding color-based segmentation

## Limitations
- Requires stable background
- Sensitive to lighting changes
- Works best with specific colors
- Real-time processing may lag on slow systems
- Cloth must cover desired area completely

## Advanced Modifications

### Add Multiple Color Detection
```python
# Detect red OR blue
mask_red = cv2.inRange(hsv, lower_red, upper_red)
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask = cv2.bitwise_or(mask_red, mask_blue)
```

### Improve Edge Smoothing
```python
mask = cv2.GaussianBlur(mask, (5, 5), 0)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
```

### Add Feathering Effect
```python
mask = cv2.blur(mask, (15, 15))
mask_inv = cv2.bitwise_not(mask)
```

## Next Steps
- Implement dynamic background update
- Add automatic color calibration
- Support multiple simultaneous cloaks
- Optimize for mobile devices
- Add special effects (sparkles, transitions)

## License
Open source - MIT License

## Credits
Inspired by Harry Potter's Invisibility Cloak and OpenCV tutorials.
