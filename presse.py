# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: presse.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import cv2
import numpy as np
import pyautogui
import time
import keyboard
import threading
left, top, width, height = (686, 860, 547, 34)
green_zone_start = 0.45
green_zone_end = 0.55

def capture_screen_region(left, top, width, height):
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def detect_slider_position(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2
    return None

def zero_stage(capture_screen_region, detect_slider_position, running_event):
    time.sleep(2)
    pyautogui.press('e')
    time.sleep(2)
    prev_slider_positions = []
    slider_velocity = 0

    while running_event.is_set():
        screenshot = capture_screen_region(left, top, width, height)
        slider_pos = detect_slider_position(screenshot)

        if slider_pos is not None:
            prev_slider_positions.append(slider_pos)

            if len(prev_slider_positions) > 10:
                prev_slider_positions = prev_slider_positions[-10:]

            if len(prev_slider_positions) > 1:
                # Calculate the velocity of the slider
                slider_velocity = (prev_slider_positions[-1] - prev_slider_positions[0]) / len(prev_slider_positions)

            # Predict the position of the slider using the calculated velocity
            predicted_pos = slider_pos + slider_velocity * 0.05  # Assuming time.sleep(0.1)

            green_zone_start_px = int(width * green_zone_start)
            green_zone_end_px = int(width * green_zone_end)

            if green_zone_start_px <= predicted_pos <= green_zone_end_px:
                pyautogui.press('space')
                print('Ползунок в зеленой зоне! Завершаем этап.')
                break

        time.sleep(0.1)
    time.sleep(2)

if __name__ == '__main__':
    running_event = threading.Event()
    running_event.set()
    try:
        zero_stage(capture_screen_region, detect_slider_position, running_event)
    except KeyboardInterrupt:
        running_event.clear()