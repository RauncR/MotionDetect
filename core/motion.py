import cv2
import os
from datetime import datetime
from .video_recorder import VideoRecorder


def save_frame(frame, output_dir):
    """Save frame with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S_%f")
    filename = os.path.join(output_dir, f"{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Motion detected: {filename}")

def detect_motion(video_path, output_dir, enabled_regions):
    """
    Main motion detection function.
        video_path (str): Path to input video.
        output_dir (str): Folder to save frames.
        regions (dict): Dictionary of regions with keys:
                        'x_start', 'x_end', 'y_start', 'y_end', 'enabled', 'sensitivity'
    """
    # --- If no output - creates, if there is - ok ---
    os.makedirs(output_dir, exist_ok=True)

    # --- Capture the very first frame, VideoCapture opens a decoder + stream ---
    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    if not ret:
        raise RuntimeError(f"Video capture failed: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    recorder = VideoRecorder(fps=fps)

    # --- Convert to grayscale (one value per pixel), gray ≈ 0.114*B + 0.587*G + 0.299*R ---
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # --- Apply Gaussian blur to reduce minor pixel noise ---
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)


    height, width = prev_frame.shape[:2] #Tuple of height, width, channels - BGR

    while True: #While True runs unless explicitly broken out of, error or returned.

        cooldown = cv2.getTrackbarPos("Cool. sec", "Controls")
        cooldown = max(2, cooldown)

        recorder.cooldown_seconds = cooldown


        # --- Capture next frame ---
        ret, frame = cap.read()
        if not ret:
            break

        # --- Convert RGB frame to grayscale for pixel luminance ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- Reduce pixel-level noise ---
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # --- Compute difference between previous frame and current frame ---
        diff = cv2.absdiff(prev_gray, gray)

        # --- Threshold difference: if difference > 20 → white, else black ---
        _, thresh = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=1)

        motion_detected = False

        # --- Iterate through active regions ---
        for region in enabled_regions:

            # --- Region coordinates in pixels ---
            x1 = int(region["x_start"] * width)
            x2 = int(region["x_end"] * width)
            y1 = int(region["y_start"] * height)
            y2 = int(region["y_end"] * height)

            # --- Extract region mask (2D NumPy array) ---
            region_mask = thresh[y1:y2, x1:x2]

            # --- Count non-zero pixels in the region ---
            motion_pixels = cv2.countNonZero(region_mask)

            # --- Total pixels in that region ---
            region_area = (y2 - y1) * (x2 - x1)

            if region_area <= 0:
                continue

            # --- Threshold pixels based on region sensitivity ---
            region_threshold = region_area * (100 - region["sensitivity"]) / 100

            if motion_pixels > region_threshold:
                motion_detected = True
                break

        # --- Save frame if motion detected ---
        recorder.update(frame, motion_detected)

        # --- Prepare for next iteration ---
        prev_gray = gray
    recorder.close()
    cap.release() #Close video file, release decoder resources, free file handles, prevent file locks(Windows)
