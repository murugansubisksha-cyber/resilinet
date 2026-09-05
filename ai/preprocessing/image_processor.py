import cv2
import os

# Get the project directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_PATH = os.path.join(BASE_DIR, "images", "road.jpg")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "processed_road.jpg")


# Read image
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Error: Image not found!")
    print("Please check ai/images/road.jpg")
    exit()


# Resize image
image = cv2.resize(image, (800, 500))


# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Reduce noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)


# Edge detection
edges = cv2.Canny(blur, 50, 150)


# Save processed image
cv2.imwrite(OUTPUT_PATH, edges)


print("Image processed successfully!")
print("Output saved at:")
print(OUTPUT_PATH)


# Display original image
cv2.imshow("Original Road Image", image)

# Display processed image
cv2.imshow("Edge Detection", edges)

cv2.waitKey(0)

cv2.destroyAllWindows()
