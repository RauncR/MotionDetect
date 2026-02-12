import cv2
import os
from datetime import datetime
from .video_recorder import VideoRecorder


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
    ui_base = prev_frame.copy()
    cv2.imshow("Search window", ui_base)
    cv2.waitKey(1)
    
    height, width = prev_frame.shape[:2]
    prev_region_grays = {}

    for i, region in enumerate(enabled_regions):
        x1 = int(region["x_start"] * width)
        x2 = int(region["x_end"] * width)
        y1 = int(region["y_start"] * height)
        y2 = int(region["y_end"] * height)

        roi = prev_frame[y1:y2, x1:x2]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), 0)

        prev_region_grays[i] = gray


    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30
    recorder = VideoRecorder(fps=fps)
    text = ""
    color = (0, 255, 255)
    while True: #While True runs unless explicitly broken out of, error or returned.

        cooldown = cv2.getTrackbarPos("Cool. sec", "Controls")
        cooldown = max(2, cooldown)

        recorder.cooldown_seconds = cooldown

        # --- Capture next frame ---
        ret, frame = cap.read()
        if not ret:
            break

        motion_detected = False

        # --- Iterate through active regions ---
        for i, region in enumerate(enabled_regions):

            # --- Region coordinates in pixels ---
            x1 = int(region["x_start"] * width)
            x2 = int(region["x_end"] * width)
            y1 = int(region["y_start"] * height)
            y2 = int(region["y_end"] * height)

            roi = frame[y1: y2, x1: x2]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (15, 15), 0)

            diff = cv2.absdiff(prev_region_grays[i], gray)
            _, thresh = cv2.threshold(diff, 5 ,255, cv2.THRESH_BINARY)
            thresh = cv2.dilate(thresh, None, iterations=1)

            motion_pixels = cv2.countNonZero(thresh)
            region_area = thresh.size

            region_threshold = region_area * (100 - region["sensitivity"]) / 100

            if region_area <= 0:
                continue

            if motion_pixels > region_threshold:
                motion_detected = True
                break

        # --- Save frame if motion detected ---
        recorder.update(frame, motion_detected)
        ui = ui_base.copy()

    if motion_detected:
        text = "RECORDING"
        color = (0, 0, 255)
    else:
        text = "SEARCHING..."
        color = (0, 255, 255)
    cv2.putText(ui, text, (40, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 2,
            color, 3)
    cv2.imshow("Search window", ui)
    cv2.waitKey(1)
        # --- Prepare for next iteration ---

    recorder.close()
    cap.release() #Close video file, release decoder resources, free file handles, prevent file locks(Windows)
