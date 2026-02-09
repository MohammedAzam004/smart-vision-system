import cv2
import sys

image_path = sys.argv[1] if len(sys.argv) > 1 else "sample_image.png"
img = cv2.imread(image_path)

if img is None:
    print(f"Error: Could not load image from {image_path}")
    print("Usage: python edge_detect.py <image_path>")
    sys.exit(1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(gray, 100, 200)

cv2.imshow("original", img)
cv2.imshow("edge", edge)
cv2.waitKey(0)
cv2.destroyAllWindows()