import cv2 
import numpy as np
import time

COLORS = {
    '1': {
        'name': 'Red',
        'lower1': np.array([0, 120, 70]),
        'upper1': np.array([10, 255, 255]),
        'lower2': np.array([170, 120, 70]),
        'upper2': np.array([180, 255, 255]),
        'has_two_ranges': True
    },
    '2': {
        'name': 'Blue',
        'lower1': np.array([100, 150, 50]),
        'upper1': np.array([140, 255, 255]),
        'has_two_ranges': False
    },
    '3': {
        'name': 'Green',
        'lower1': np.array([40, 50, 50]),
        'upper1': np.array([80, 255, 255]),
        'has_two_ranges': False
    },
    '4': {
        'name': 'Yellow',
        'lower1': np.array([20, 100, 100]),
        'upper1': np.array([30, 255, 255]),
        'has_two_ranges': False
    },
    '5': {
        'name': 'Black',
        'lower1': np.array([0, 0, 0]),
        'upper1': np.array([180, 255, 50]),
        'has_two_ranges': False
    }
}

print("\n" + "="*50)
print("    INVISIBILITY CLOAK - COLOR SELECTION")
print("="*50)
print("\nSelect the color of your cloak:")
for key, color in COLORS.items():
    print(f"  {key}. {color['name']}")
print("="*50)

color_choice = input("\nEnter your choice (1-5): ").strip()
if color_choice not in COLORS:
    print("Invalid choice! Defaulting to Red.")
    color_choice = '1'

selected_color = COLORS[color_choice]
print(f"\n✓ Selected: {selected_color['name']} Cloak")
print("\nStarting camera... Please step away from the frame for background capture.\n")

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
save_file = cv2.VideoWriter("invisibility_clock.avi", fourcc, 20.0, (640, 480))

time.sleep(2)
background = 0
for i in range(20):
    ret, background = cap.read()
background = np.flip(background, axis=1)

kernel = np.ones((3, 3), np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = np.flip(frame, axis=1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_1 = cv2.inRange(hsv, selected_color['lower1'], selected_color['upper1'])
    
    if selected_color['has_two_ranges']:
        mask_2 = cv2.inRange(hsv, selected_color['lower2'], selected_color['upper2'])
        mask = mask_1 + mask_2
    else:
        mask = mask_1
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    mask_inv = cv2.bitwise_not(mask)

    result_1 = cv2.bitwise_and(background, background, mask=mask)
    result_2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_output = cv2.addWeighted(result_1, 1, result_2, 1, 0)

    cv2.imshow(f"Invisibility Cloak - {selected_color['name']}", final_output)
    save_file.write(final_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
save_file.release()
cv2.destroyAllWindows()













































# Importing libraries
# import cv2 
# import numpy as np
# import time


# cv2 → OpenCV library for computer vision (reading video, processing images).

# numpy (np) → For numerical operations, arrays, creating masks, kernels.

# time → Used for delays (time.sleep) to allow camera to warm up.

# 2️⃣ Capturing video and setting up saving
# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# save_file = cv2.VideoWriter("invisibility_clock.avi", fourcc, 20.0, (640,480))


# cv2.VideoCapture(0) → Access your webcam. 0 is default camera.

# VideoWriter_fourcc(*'XVID') → Codec to save video.

# cv2.VideoWriter(...) → File where the final video will be saved.

# "invisibility_clock.avi" → Output filename

# 20.0 → Frames per second

# (640,480) → Resolution of video

# ✅ This prepares you to record the invisibility effect while showing it live.

# 3️⃣ Capturing the background
# time.sleep(2)
# background = 0
# for i in range(20):
#     ret, background = cap.read()
# background = np.flip(background, axis=1)


# time.sleep(2) → Wait 2 seconds so camera adjusts to light.

# for i in range(20) → Capture 20 frames to get a stable background.

# np.flip(background, axis=1) → Mirror the background, so it matches flipped live frames.

# Why background?

# To “replace” the cloak color with this background, creating the invisibility illusion.

# 4️⃣ Creating a kernel for morphology operations
# kernel = np.ones((3,3), np.uint8)


# A small 3x3 matrix of ones.

# Used for morphological operations like opening and dilation to clean up the mask.

# np.uint8 → 8-bit integers, required for OpenCV masks.

# 5️⃣ Main loop: reading live frames
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break


# cap.isOpened() → Checks if camera is available.

# cap.read() → Reads a single frame from the webcam.

# ret → True if the frame is captured.

# frame → The actual image captured.

# if not ret: break → Stop the loop if webcam fails.

# 6️⃣ Flipping the frame
# frame = np.flip(frame, axis=1)


# Mirror the frame horizontally for mirror-like effect.

# Makes it look more natural for the user, like a mirror.

# 7️⃣ Converting to HSV color space
# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


# OpenCV reads images in BGR format by default.

# HSV = Hue, Saturation, Value

# Easier to detect colors (like red) compared to BGR, because hue isolates the color.

# 8️⃣ Creating masks for red color
# lower_red = np.array([0,120,70])
# upper_red = np.array([10,255,255])
# mask_1 = cv2.inRange(hsv, lower_red, upper_red)

# lower_red = np.array([170,120,70])
# upper_red = np.array([180,255,255])
# mask_2 = cv2.inRange(hsv, lower_red, upper_red)

# mask = mask_1 + mask_2


# Red color in HSV is split across two ranges:

# 0–10 (lower red)

# 170–180 (upper red)

# cv2.inRange() → Creates a binary mask:

# Pixels in range → 255 (white)

# Pixels out of range → 0 (black)

# mask = mask_1 + mask_2 → Combine the two masks into one.

# ✅ This mask identifies all red pixels (the cloak).

# 9️⃣ Cleaning the mask
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
# mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)


# MORPH_OPEN → Removes small noise from mask.

# MORPH_DILATE → Enlarges detected area for better coverage.

# This ensures the red cloak area is smooth and continuous in the mask.

# 10️⃣ Creating the inverse mask
# mask_inv = cv2.bitwise_not(mask)


# mask_inv = everything not red.

# Needed to combine the live frame and the background properly.

# 11️⃣ Combining background and live frame
# result_1 = cv2.bitwise_and(background, background, mask=mask)
# result_2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
# final_output = cv2.addWeighted(result_1, 1, result_2, 1, 0)


# result_1 → Keeps background only where cloak is detected.

# result_2 → Keeps original frame where cloak is not present.

# cv2.addWeighted() → Combines both layers into one frame.

# ✅ This is the magic step that makes the cloak appear invisible.

# 12️⃣ Showing and saving the final output
# cv2.imshow("Invisibility Cloak", final_output)
# save_file.write(final_output)


# cv2.imshow() → Shows live invisibility effect.

# save_file.write() → Saves each frame to the output video.

# 13️⃣ Exit on key press
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break


# waitKey(1) → Wait 1 ms for key press.

# ord('q') → Quit if the user presses q.

# 14️⃣ Cleanup
# cap.release()
# save_file.release()
# cv2.destroyAllWindows()


# Release the webcam and the video writer.

# Close all OpenCV windows to free resources.