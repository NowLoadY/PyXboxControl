"""
这是一个Xbox手柄的Python库，可以用来读取手柄的状态并控制手柄震动
使用方法：
1. 导入库
   from my_xbox_handle import XboxController
2. 创建XboxController对象
   xbox_controller = XboxController()
3. 读取手柄状态
   joystick_state, button_state = xbox_controller.get_joystick_state()
   joystick_state是一个字典，包含了摇杆的各个状态，例如：
   {'x_axis_left': 0, 'y_axis_left': 0, 'x_axis_right': 0, 'y_axis_right': 0, 'LT': 0, 'RT': 0}
   button_state也是一个字典，包含了手柄上各个按钮的状态，例如：
   {'A': False, 'B': False, 'X': False, 'Y': False, 'LB': False, 'RB': False, 'task': False, 'settings': False, 'left_axis_button': False, 'right_axis_button': False}
4. 控制手柄震动
   xbox_controller.set_vibration(left_motor, right_motor, controller_id=0)
   left_motor和right_motor是震动电机的强度，范围是0到1，0表示关闭震动，1表示最大强度
   controller_id是手柄的编号，如果只有一个手柄，可以不用指定，默认为0
"""

import pygame
import ctypes
import time
import math
import threading

pygame.init()
xinput = ctypes.windll.xinput1_4  # Load Xinput.dll


# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]


# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint
ERROR_DEVICE_NOT_CONNECTED = 1167
ERROR_SUCCESS = 0


class XboxController:
    def __init__(self, device_id=0, deadzone=3):
        self.device_id = device_id
        self.LONG_PRESS_TIME = 100
        self.controller = pygame.joystick.Joystick(device_id)
        self.controller.init()
        self.joystick_deadzone = deadzone  # 摇杆死区
        self.vibration_user = {}
        self.button_names = {0: 'A', 1: 'B', 2: 'X', 3: 'Y',
                             4: 'LB', 5: 'RB',
                             6: 'task', 7: 'settings',
                             8: 'left_axis_button', 9: 'right_axis_button'}
        self.joystick_state = {'x_axis_left': 0, 'y_axis_left': 0, 'x_axis_right': 0, 'y_axis_right': 0,
                               'LT': 0,
                               'RT': 0}
        self.button_state = {'A': False, 'B': False,
                             'X': False, 'Y': False,
                             'LB': False, 'RB': False,
                             'task': False, 'settings': False,
                             'left_axis_button': False, 'right_axis_button': False}
        self.button_press_times = {button_name: None for button_name in self.button_names.values()}
        left_strength = 1
        right_strength = 1
        for i in range(2):
            self.set_vibration(left_strength, right_strength)
            time.sleep(0.1)
            self.set_vibration(0, 0)
            time.sleep(0.1)

    def get_joystick_state(self):

        self.button_state = {button_name: self.button_state.get(self.button_names.get(i)) for i, button_name in
                             self.button_names.items()}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.JOYBUTTONDOWN:
                for i in range(self.controller.get_numbuttons()):
                    if self.controller.get_button(i):
                        button_name = self.button_names.get(i)
                        self.button_state[button_name] = True
                        self.button_press_times[button_name] = pygame.time.get_ticks()
            if event.type == pygame.JOYBUTTONUP:
                for i in range(self.controller.get_numbuttons()):
                    if not self.controller.get_button(i):
                        button_name = self.button_names.get(i)
                        if button_name is not None:
                            self.button_state[button_name] = False
                            if self.button_press_times[button_name] is not None:
                                press_duration = pygame.time.get_ticks() - self.button_press_times[button_name]
                                if press_duration >= self.LONG_PRESS_TIME:
                                    self.button_state[f'{button_name}_long_press'] = True
                                self.button_press_times[button_name] = None
            if event.type == pygame.JOYAXISMOTION:
                self.joystick_state['x_axis_left'] = int(self.controller.get_axis(0) * 50)
                self.joystick_state['y_axis_left'] = int(self.controller.get_axis(1) * 50)
                self.joystick_state['x_axis_right'] = int(self.controller.get_axis(2) * 50)
                self.joystick_state['y_axis_right'] = int(self.controller.get_axis(3) * 50)
                self.joystick_state['LT'] = int(self.controller.get_axis(4) * 50 + 50)
                self.joystick_state['RT'] = int(self.controller.get_axis(5) * 50 + 50)
                # Apply deadzone to joystick values
                for axis_name, axis_value in self.joystick_state.items():
                    if isinstance(axis_value, (int, float)) and abs(axis_value) < self.joystick_deadzone:
                        self.joystick_state[axis_name] = 0
            if event.type == pygame.JOYHATMOTION:
                self.joystick_state['dpad'] = self.controller.get_hat(0)
        return self.joystick_state, self.button_state

    def set_vibration(self, left_motor, right_motor, controller_id=0):
        vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
        XInputSetState(controller_id, ctypes.byref(vibration))

    def event_vibration_feedback(self, event):
        self.vibration_user["event_vibration_feedback"] = None
        if event == "success":
            self.set_vibration(1, 1, self.device_id)
            time.sleep(0.2)
            self.set_vibration(0, 0, self.device_id)
            time.sleep(0.15)
            self.set_vibration(0.1, 0.2, self.device_id)
            time.sleep(0.1)
            self.set_vibration(1, 1, self.device_id)
            time.sleep(0.25)
            self.set_vibration(0, 0, self.device_id)
        elif event == "heavy":
            self.set_vibration(1, 1, self.device_id)
            time.sleep(0.3)
            self.set_vibration(0, 0, self.device_id)
        elif event == "light":
            self.set_vibration(0, 0.5, self.device_id)
            time.sleep(0.3)
            self.set_vibration(0, 0, self.device_id)
        elif event == "fail":
            self.set_vibration(0, 1, self.device_id)
            time.sleep(0.15)
            self.set_vibration(0, 0, self.device_id)
            time.sleep(0.1)
            self.set_vibration(0, 1, self.device_id)
            time.sleep(0.15)
            self.set_vibration(0, 0, self.device_id)
        elif event == "switch":
            self.set_vibration(1, 0, self.device_id)
            time.sleep(0.3)
            self.set_vibration(0, 1, self.device_id)
            time.sleep(0.3)
            self.set_vibration(1, 0, self.device_id)
            time.sleep(0.3)
            self.set_vibration(0, 1, self.device_id)
            time.sleep(0.3)
            self.set_vibration(0, 0, self.device_id)
        elif event == "back":
            for i in range(10):
                self.set_vibration(max(1-i/6, 0), 1-i/10, self.device_id)
                time.sleep(0.1)
            self.set_vibration(0, 0, self.device_id)
        elif event == "come":
            for i in range(7):
                self.set_vibration(min(i / 7, 1), min(i / 3, 1), self.device_id)
                time.sleep(0.1)
            for i in range(3):
                self.set_vibration(min(1 - i/3, 1), min(1 - i/3, 1))
                time.sleep(0.1)
            self.set_vibration(0, 0, self.device_id)
        self.vibration_user.clear()
