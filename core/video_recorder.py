import cv2
import os
import time
from datetime import datetime


class VideoRecorder:
    """
    Motion triggered video recorder with cooldown logic.
    """

    def __init__(self, fps, codec="mp4v"):
        self.fps = fps
        self.codec = codec
        self.cooldown_seconds = 0

        self.writer = None
        self.output_dir = None
        self.output_path = None
        self.frame_size = None

        self.recording = False
        self.last_motion_time = None

        self.base_dir = os.path.join(os.getcwd(), "recordings")
        self.no_motion_frames = 0

    # -------------------------------------------------------------

    def _start_new_recording(self, frame):
        if self.recording:
            return

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

        os.makedirs(self.base_dir, exist_ok=True)

        self.output_dir = os.path.join(self.base_dir, timestamp)
        os.makedirs(self.output_dir, exist_ok=True)

        self.output_path = os.path.join(self.output_dir, "motion.mp4")

        h, w = frame.shape[:2]
        self.frame_size = (w, h) #  Width - height

        fourcc = cv2.VideoWriter_fourcc(*self.codec)

        self.writer = cv2.VideoWriter(
            self.output_path,
            fourcc,
            self.fps,
            self.frame_size
        )

        if not self.writer.isOpened():
            raise RuntimeError("Failed to open video writer")

        self.recording = True
        self.last_motion_time = time.time()

        print(f"Recording started: {self.output_path}")

    # -------------------------------------------------------------

    def update(self, frame, motion_detected):
        now = time.time()

        # --- Motion appeared ---
        if motion_detected:
            self.last_motion_time = now
            self.no_motion_frames = 0
            if not self.recording:
                self._start_new_recording(frame)
        else:
            self.no_motion_frames += 1

        # --- Write if recording ---
        if self.recording:
            self.writer.write(frame)


            # --- Check cooldown ---
            if not motion_detected:
                if self.no_motion_frames >= int(self.fps * self.cooldown_seconds):
                    self.close()

    # -------------------------------------------------------------

    def close(self):
        if not self.recording:
            return

        self.writer.release()
        self.writer = None
        self.recording = False

        print(f"Recording finished: {self.output_path}")