# noinspection PyInterpreter
import cv2
import numpy as np

sensitivity_trackbar = "Sens. %"
cooldown_trackbar = "Cool. sec"
def configure_regions(regions, background_frame = None):
    active_region_id = 1
    """
    OpenCV-based UI to toggle regions and adjust sensitivity.
    Args:
        regions (dict): dictionary of regions
    Returns:
        dict: updated regions
    """
    # --- Blank canvas required for keyboard input, trackbars, mouse events---
    if background_frame is not None:
        canvas_base = background_frame.copy()
    else:
        canvas_base = np.zeros((400, 600, 3), dtype=np.uint8)

    cv2.namedWindow("Select regions", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("Select regions", 950, 600)

    # --- Window for trackbar (sensitivity) ---
    cv2.namedWindow("Controls")
    cv2.createTrackbar(
        sensitivity_trackbar, #Name of the trackbar
        "Controls", #Window name
        int(regions[active_region_id]["sensitivity"]), #Initial position
        100,
        lambda x: None  # otherwise mandatory callback not needed; read directly later
    )
    cv2.createTrackbar(
        cooldown_trackbar,
        "Controls",
        10, #  Initial value
        60, #  max value
        lambda x: None
    )

    print("Press keys 1–5 to toggle regions. Press Enter to confirm.")

    while True:
        canvas = canvas_base.copy()

        h, w = canvas.shape[:2]

        for rid, region in regions.items():
            border_padding = 2

            # --- Pixel coordinates ---
            x1 = int(region["x_start"] * w) + border_padding
            x2 = int(region["x_end"] * w) - border_padding
            y1 = int(region["y_start"] * h) + border_padding
            y2 = int(region["y_end"] * h) - border_padding

            color = (0, 255, 0) if region["enabled"] else (0, 0, 255)
            thickness = 2

            # --- Draw rectangle ---
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, thickness)

            # --- Draw text on top-left of rectangle ---
            status = "ENABLED" if region["enabled"] else "DISABLED"
            msg = f"{rid}: {region['name']}"
            msg2 = f"{status}"
            msg3 = f"Sensitivity {region['sensitivity']}"
            cv2.putText(canvas, msg, (x1 + 5, y1 + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(canvas, msg2, (x1 + 5, y1 + 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(canvas, msg3, (x1 + 5, y1 + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # --- Instructions at bottom ---
        cv2.putText(canvas, "Press 1-5 to toggle regions, ENTER to continue",
                    (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 200, 200), 2)
        # --- Show/update canvas for region selection ---
        cv2.imshow("Select regions", canvas)
        key = cv2.waitKey(45) & 0xFF #Listen explicitly for keys, stops loop for 45ms

        if key == 13:  # ASCII for 'Enter'
            break

        # --- Select region by number keys ---
        if key in [ord(str(i)) for i in range(1, 6)]: #ord(str) returns int of the ASCII value
            active_region_id = key - ord('0')

            # --- Toggle enable/disable ---
            regions[active_region_id]["enabled"] = not regions[active_region_id]["enabled"]

            # --- Sync trackbar to active region sensitivity ---
            current = int(regions[active_region_id]["sensitivity"])
            cv2.setTrackbarPos(sensitivity_trackbar, "Controls", current) #Sets the trackbar value

            print(f'Region {active_region_id} '
                  f'{"ENABLED" if regions[active_region_id]["enabled"] else "DISABLED"}')

        # --- Read sensitivity for active region ---
        raw = cv2.getTrackbarPos(sensitivity_trackbar, "Controls")
        raw = max(1, min(raw, 99))
        regions[active_region_id]["sensitivity"] = raw

    enabled_regions = [r for r in regions.values() if r["enabled"]]

    if not enabled_regions:
        print("No regions selected → using full frame")

        #Read current track bar
        raw = cv2.getTrackbarPos(sensitivity_trackbar, "Controls")
        raw = max(raw, 1) #Prevent zero

        enabled_regions = [{
            "name": "full_frame",
            "enabled": True,
            "x_start": 0.0,
            "x_end": 1.0,
            "y_start": 0.0,
            "y_end": 1.0,
            "sensitivity": raw
        }]
    cv2.destroyWindow("Select regions")
    return enabled_regions
