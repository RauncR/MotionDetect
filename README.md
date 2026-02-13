ThiefBuster 2000 – Smart Motion Clip Generator

Automatically detects motion in video files and generates video clips of activity.
Users can define multiple Regions of Interest (ROIs), set per-region sensitivity and have the app search for motion.

Features
ROI-based motion detection: Top-left, top-right, bottom-left, bottom-right, and center each ROI's sensitivity can be adjusted by the user.
Adjustable cooldown in seconds: Prevents multiple clips for continuous movement.
Clips are saved automatically in the app directory.
Status messages indicate recording progress and completion.

How It Works

User Input: Select a video file.
UI and ROI Setup: First frame is displayed for the user up to 5 ROI's or if no ROI is selected - full screen is searched.


Frame Processing:
Convert frames to grayscale
Apply blur to reduce noise
Compare against a background reference (previous frame)
Threshold and dilate differences to highlight motion

Motion Evaluation: Each ROI calculates motion separately.
Motion triggers recording, cooldown logic and expansion buffer manage clip length.
User Feedback: Status messages display current recording state; app closes when done.

Tech Stack
Python – Core language
OpenCV – Video and image processing
NumPy – Numerical computations
FFmpeg – Video clip generation
Tkinter – User interface

Usage
Launch the app.
Select video file.
Adjust ROIs and sensitivities, when done press ENTER.
"SEARCHING" is displayed.
When motion is detected and clip starts recording "RECORDING" blinks.


Possible problems
