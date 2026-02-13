#ThiefBuster 2000 – Smart Motion Clip Generator  

- Automatically detects motion in video files and generates video clips of activity.  
- Users can define multiple Regions of Interest (ROIs), set per-region sensitivity and have the app search for motion.  

##Features  
- ROI-based motion detection: Top-left, top-right, bottom-left, bottom-right, and center each ROI's sensitivity can be adjusted by the user.  
- Adjustable cooldown in seconds: Prevents multiple clips for continuous movement.  
- Clips are saved automatically in the app directory.  
- Status messages indicate recording progress and completion.  

##How It Works  

- User Input: Select a video file.  
- UI and ROI Setup: First frame is displayed for the user up to 5 ROI's or if no ROI is selected - full screen is searched.  
- Frame Processing:  
- Convert frames to grayscale   
- Apply blur to reduce noise    
- Compare against a background reference (previous frame)    
- Threshold and dilate differences to highlight motion  

- Motion Evaluation: Each ROI calculates motion separately.  
- Motion triggers recording, cooldown logic and expansion buffer manage clip length.  
- User Feedback: Status messages display current recording state; app closes when done.  

##Tech Stack  
- Python – Core language  
- OpenCV – Video and image processing  
- NumPy – Numerical computations  
- FFmpeg – Video clip generation  
- Tkinter – User interface  

##Usage  
- Launch the app.  
- Select video file.  
- Adjust ROIs and sensitivities, when done press ENTER.  
- "SEARCHING" is displayed.  
- When motion is detected and clip starts recording "RECORDING" blinks.
- App closes when done  


##Possible problems and their solutions:  
After grayscale and blur pixel shade of gray change is compared against same pixel in previous frame. Shade of gray varies from black:0 to white:255. Point of decision can be set i.e 20 which allow minor pixel changes and helps to reduce noise.  
It can also be lowered to "increase sensitivity" and completely avoid skipping movements. At the same time dilate iterations can also greatly increase sensitivity. User set sensitivity is only "percentage of changed pixels against whole pixels of ROI" to trigger motion.  
App logic tilts towards making code sensitive and give more responsibility for user to set desired sensitivity.   

Frame count is introduced to avoid 2 second clips. User sets it as cooldown in seconds which literally is (fps * seconds) - if that amount of frames will not trigger motion, clip is saved.  

##Future Improvements  

Big picture on a high level: User launches the app (i.e ThiefBuster2000.exe) and is prompted to select either file search or live search. We have file search, but live screen monitoring should be written and introduced to completely avoid necessity for video exports   from different interfaces. User would draw a main frame box - usually complete camera view and then ROI (or perhaps several ROIs) and commands program on surveillance. if motion detected - clip saved. Features would be similar to current app.  

Opening a dedicated folder as app finishes.  
