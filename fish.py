# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: fish.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import cv2
import numpy as np
import pyautogui
import time
import threading

def fish_stage(search_region, template_path, running_event):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::(-1)]
    try:
        while running_event.is_set():
            screenshot = pyautogui.screenshot(region=search_region)
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            _, binary_frame = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)
            res = cv2.matchTemplate(binary_frame, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.7)
            if len(loc[0]) > 0:
                pyautogui.press('space')
                print('Пробел нажат из-за найденного шаблона')
                time.sleep(2)
                return
            time.sleep(0.1)

    except KeyboardInterrupt:
        print('Программа была остановлена пользователем.')
        return
if __name__ == '__main__':
    running_event = threading.Event()
    running_event.set()
    search_region = (834, 1017, 251, 30)
    template_path = 'images/kluet.png'
    try:
        fish_stage(search_region=search_region, template_path=template_path, running_event=running_event)
    except KeyboardInterrupt:
        running_event.clear()
    running_event.clear()