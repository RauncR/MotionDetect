import tkinter as tk
"""Python standard GUI(Graphical User Interface) library
provides windows, buttons, dialogs and event loops"""

from tkinter import filedialog
"""Imports only the file dialog module, it provides:
- open file dialogs
- save dialogs
- folder selectors"""


def select_videos():
    """Creates the Tkinter application instance, required for any Tkinter UI to exist
    Even though window is not seen yet, Tkinter cannot show dialogs without a root."""
    root = tk.Tk()

    """Immediately hides the main Tk window
       Prevents an empty useless GUI window from appearing
       The app still exists — it’s just invisible"""
    root.withdraw()

    """Opens a native OS file picker
       Blocks execution until user finishes
       Returns selected file paths"""
    file_paths = filedialog.askopenfilenames(
        title="Fail sjuda b6straa!",  # Dialog window title
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]  # Filetypes is a list of tuples, *.* - show all
    )
    return list(file_paths)  # Returns absolute paths as tuple of strings