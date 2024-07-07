# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import subprocess
import pygetwindow as gw
import keyboard
import fish
from tyanet import second_stage
from presse import zero_stage
import threading
import os
from datetime import datetime
from tkinter import font
import subprocess
import presse
from tyanet import second_stage, detect_camera_movement
from presse import zero_stage, detect_slider_position, capture_screen_region

class App:
    def __init__(self, master):
        self.master = master
        master.title('hcked by raywom')
        master.geometry('500x300')
        self.setup_interface()

    def setup_interface(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack(expand=True)
        self.label = tk.Label(button_frame,
                              text='ВНИМАНИЕ! ВЗЛОМАНО)')
        self.label.pack()
        self.run_button = tk.Button(button_frame, text='Старт', command=self.run_program)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.run_hotkey_label = tk.Label(button_frame, text='(Горячая клавиша: +)')
        self.run_hotkey_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button = tk.Button(button_frame, text='Стоп', command=self.stop_program, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_hotkey_label = tk.Label(button_frame, text='(Горячая клавиша: -)')
        self.stop_hotkey_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
        keyboard.add_hotkey('+', self.run_program)
        keyboard.add_hotkey('-', self.stop_program)
        self.running_event = threading.Event()
        self.running_event.set()

    def run_program(self):
        self.running_event.set()
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.execute_program)
        self.thread.start()

    def show_message(self, title, message, msg_type='info'):
        if msg_type == 'info':
            messagebox.showinfo(title, message)
        else:  # inserted
            if msg_type == 'warning':
                messagebox.showwarning(title, message)
            else:  # inserted
                if msg_type == 'error':
                    messagebox.showerror(title, message)

    def on_closing(self):
        if messagebox.askokcancel('Выход', 'Вы уверены, что хотите выйти?'):
            self.stop_program()
            self.master.destroy()

    def activate(self):
        self.setup_interface()

    def stop_program(self):
        self.running_event.clear()
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def execute_program(self):
        try:
            while self.running_event.is_set():
                target_window = None
                for window in gw.getAllWindows():
                    if 'Majestic RP' in window.title:
                        target_window = window
                        break
                if target_window:
                    break
                if target_window is None:
                    self.show_message('Ошибка', 'Игра не запущена!', 'warning')
                    self.stop_program()
                    return
        except Exception as e:
            error_message = f'Произошла ошибка: {str(e)}'
            self.show_message('Ошибка', error_message, 'error')
            self.stop_program()
        else:  # inserted
            window_x, window_y, window_width, window_height = (
            target_window.left, target_window.top, target_window.width, target_window.height)
            search_region = (window_x, window_y, window_width, window_height)
            template_path = 'C:/Users/nomad/RYBAK/pythonProject/.venv/cheat/images/kluet.png'
            completed_stages = []
            while self.running_event.is_set():
                if presse.zero_stage not in completed_stages:
                    presse.zero_stage(capture_screen_region, detect_slider_position, self.running_event)
                    completed_stages.append(presse.zero_stage)
                else:  # inserted
                    if fish.fish_stage not in completed_stages:
                        fish.fish_stage(search_region, template_path, self.running_event)
                        completed_stages.append(fish.fish_stage)
                    else:  # inserted
                        if second_stage not in completed_stages:
                            second_stage(self.running_event, 'C:/Users/nomad/RYBAK/pythonProject/.venv/cheat/images/finish.png',
                                         detect_camera_movement=detect_camera_movement)
                            completed_stages.append(second_stage)
                            completed_stages = []
                if keyboard.is_pressed('esc'):
                    self.show_message('Программа завершена', 'Программа завершена пользователем.', 'info')
                    self.stop_program()


    def on_closing(self):
        if messagebox.askokcancel('Выход', 'Вы уверены, что хотите выйти?'):
            self.stop_program()
            self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
