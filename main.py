import cv2

from core.motion import detect_motion
from ui.file_selector import select_videos
from ui.region_selector import configure_regions

def main():
    regions = {
        1: {"name": "Top left", "enabled": False, "x_start": 0.0, "x_end": 0.5, "y_start": 0.0, "y_end": 0.5, "sensitivity": 95},
        2: {"name": "Top right", "enabled": False, "x_start": 0.5, "x_end": 1.0, "y_start": 0.0, "y_end": 0.5, "sensitivity": 95},
        3: {"name": "Bottom left", "enabled": False, "x_start": 0.0, "x_end": 0.5, "y_start": 0.5, "y_end": 1.0, "sensitivity": 95},
        4: {"name": "Bottom right", "enabled": False, "x_start": 0.5, "x_end": 1.0, "y_start": 0.5, "y_end": 1.0, "sensitivity": 95},
        5: {"name": "Center", "enabled": False, "x_start": 0.33, "x_end": 0.66, "y_start": 0.33, "y_end": 0.66, "sensitivity": 95}
    }

    videos = select_videos()
    if not videos:
        print("No videos selected")
        return

    cap = cv2.VideoCapture(videos[0])
    ret, first_frame = cap.read()
    cap.release()
    if not ret:
        print("Failed to read video")
        return

    regions = configure_regions(regions, background_frame = first_frame)

    for video_path in videos:
        detect_motion(video_path, output_dir="output", enabled_regions=regions)

if __name__ == "__main__":
    main()
