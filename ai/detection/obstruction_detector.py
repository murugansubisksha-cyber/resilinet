import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_PATH = os.path.join(BASE_DIR, "images", "road.jpg")
OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "output",
    "obstruction_detection.jpg"
)


# Read image
image = cv2.imread(IMAGE_PATH)

if image is None:
    print("Error: Road image not found!")
    exit()


# Resize image
image = cv2.resize(image, (800, 500))

# Keep a copy
original = image.copy()


# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Blur image
blur = cv2.GaussianBlur(gray, (5, 5), 0)


# Edge detection
edges = cv2.Canny(blur, 30, 100)


# Connect nearby edges
kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (5, 5)
)

dilated = cv2.dilate(
    edges,
    kernel,
    iterations=2
)


# Find contours
contours, _ = cv2.findContours(
    dilated,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


object_count = 0


for contour in contours:

    area = cv2.contourArea(contour)

    # Ignore very small contours
    if area > 100:

        x, y, w, h = cv2.boundingRect(contour)

        # Ignore extremely thin objects
        if w > 20 and h > 20:

            cv2.rectangle(
                original,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            cv2.putText(
                original,
                "Possible Object",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2
            )

            object_count += 1


# Display count
cv2.putText(
    original,
    f"Possible Objects: {object_count}",
    (20, 35),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 0, 0),
    2
)


# Save result
cv2.imwrite(OUTPUT_PATH, original)


print("Detection completed!")
print(f"Possible objects detected: {object_count}")
print(f"Output saved at: {OUTPUT_PATH}")


# Show windows
cv2.imshow("Original Image", image)
cv2.imshow("Edges", edges)
cv2.imshow("Dilated Edges", dilated)
cv2.imshow("Possible Object Detection", original)

cv2.waitKey(0)
cv2.destroyAllWindows()