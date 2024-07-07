import cv2
import numpy as np
import keyboard
import pyautogui
import time
import threading

def enhance_contrast(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(image)

def detect_camera_movement(frame1, frame2, lower_half_only=True):
    if lower_half_only:
        screen_width, screen_height = pyautogui.size()
        lower_half_region = (0, 0, screen_width, screen_height // 2)
        frame1 = pyautogui.screenshot(region=lower_half_region)
        frame2 = pyautogui.screenshot(region=lower_half_region)
    frame1 = np.array(frame1)
    frame2 = np.array(frame2)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray1 = enhance_contrast(gray1)
    gray2 = enhance_contrast(gray2)
    flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.2, 3, 15, 3, 5, 1.2, 0)
    if flow is None or flow.size == 0:
        return (0, 0)
    mean_flow = np.mean(flow, axis=(0, 1))
    return mean_flow

def second_stage(running_event, template_path, detect_camera_movement):
    is_a_pressed = False
    is_d_pressed = False
    try:
        while running_event.is_set():
            mean_flow = detect_camera_movement(None, None)
            move_x = mean_flow[0]
            if move_x > 0:
                direction = 'left'
            elif move_x < 0:
                direction = 'right'
            else:
                direction = 'none'
            if direction != 'none':
                if is_a_pressed:
                    keyboard.release('a')
                    is_a_pressed = False
                elif is_d_pressed:
                    keyboard.release('d')
                    is_d_pressed = False
                if direction == 'left':
                    keyboard.press('d')
                    is_d_pressed = True
                else:
                    keyboard.press('a')
                    is_a_pressed = True
                print('Направление движения камеры:', direction)
            print('Проверка на наличие шаблона на экране...')
            try:
                location = pyautogui.locateOnScreen(template_path, confidence=0.7)
            except Exception as e:
                location = None
            if location:
                print(f'Шаблон обнаружен на позиции: {location}, выполнение действий перед завершением программы.')
                time.sleep(3)
                keyboard.release('a')
                keyboard.release('d')
                pyautogui.click(970, 705)
                time.sleep(2)
                break
            else:
                print('Шаблон не обнаружен.')
                time.sleep(0.5)
    except KeyboardInterrupt:
        print('Программа была остановлена пользователем.')
        if is_a_pressed:
            keyboard.release('a')
        if is_d_pressed:
            keyboard.release('d')
            
if __name__ == '__main__':
    running_event = threading.Event()
    running_event.set()
    template_path = 'C:/Users/nomad/RYBAK/pythonProject/.venv/cheat/images/finish.png'
    try:
        second_stage(running_event, template_path, detect_camera_movement)
    except KeyboardInterrupt:
        running_event.clear()
    running_event.clear()