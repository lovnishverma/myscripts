import cv2
import time
import datetime
import os

# Optional: plays a sound when motion is detected
try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

# Create output folder
output_folder = "motion_captures"
os.makedirs(output_folder, exist_ok=True)

# Initialize webcam
cam = cv2.VideoCapture(0)
time.sleep(2)  # Allow camera to warm up

# Read initial frames
ret, frame1 = cam.read()
ret, frame2 = cam.read()

motion_detected = False

print("[INFO] Starting motion detection. Press 'q' to quit.")

while True:
    # Frame difference
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        # Draw rectangle around motion area
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True

    # Show live video feed
    cv2.imshow("Motion Detector", frame1)

    if motion_detected:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_folder}/motion_{timestamp}.jpg"
        cv2.imwrite(filename, frame1)
        print(f"[ALERT] Motion Detected! Snapshot saved to {filename}")

        if SOUND_ENABLED:
            playsound("alert.mp3")  # Provide your own sound file

        break  # Exit after detection (or remove this to keep monitoring)

    # Update frames
    frame1 = frame2
    ret, frame2 = cam.read()

    # Exit on 'q' press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()
