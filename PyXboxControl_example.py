import math
import time

import my_xbox_handle


# Here you can add your own code to control the ship using the Xbox controller.

# 手柄反馈
def handle_work():
    joystick_state, button_state = XboxController.get_joystick_state()
    # -------------------------#
    # LT、RT控制下降和上升
    # -------------------------#
    param1 = joystick_state.get('LT')
    param2 = joystick_state.get('RT')
    ############################################## vibration start
    if len(XboxController.vibration_user) == 0:  # 震动
        if param1 != 0 or param2 != 0:
            left_strength = param1 / 100
            right_strength = param2 / 100
            XboxController.set_vibration(left_strength, right_strength)
            XboxController.vibration_user["LT_RT"] = "both"
        else:
            XboxController.vibration_user.clear()
    elif len(XboxController.vibration_user) != 0:
        if "LT_RT" in XboxController.vibration_user:
            if param1 != 0 or param2 != 0:
                left_strength = param1 / 100
                right_strength = param2 / 100
                XboxController.set_vibration(left_strength, right_strength)
            else:
                XboxController.set_vibration(0, 0)
                XboxController.vibration_user.clear()
    ##############################################
    ##############################################
    # -------------------------#
    # 左摇杆控制平移
    # -------------------------#
    param1 = joystick_state.get('x_axis_left')
    param2 = joystick_state.get('y_axis_left')
    ############################################## vibration start
    if len(XboxController.vibration_user) == 0:  # 震动
        if param1 != 0 or param2 != 0:
            left_strength = min((math.sqrt(param1 ** 2 + param2 ** 2)) / 50, 1)
            right_strength = 0
            XboxController.set_vibration(left_strength, right_strength)
            XboxController.vibration_user["axis_left"] = "left"
        else:
            XboxController.vibration_user.clear()
    elif len(XboxController.vibration_user) != 0:
        if "axis_left" in XboxController.vibration_user:
            if param1 != 0 or param2 != 0:
                left_strength = min((math.sqrt(param1 ** 2 + param2 ** 2)) / 50, 1)
                right_strength = 0
                XboxController.set_vibration(left_strength, right_strength)
            else:
                XboxController.set_vibration(0, 0)
                XboxController.vibration_user.clear()
    ##############################################
    ##############################################
    # -------------------------#
    # 右摇杆控制姿态角
    # -------------------------#
    param1 = joystick_state.get('x_axis_right')
    param2 = joystick_state.get('y_axis_right')
    ############################################## vibration start
    if len(XboxController.vibration_user) == 0:  # 震动
        if param1 != 0 or param2 != 0:
            left_strength = 0
            right_strength = min((math.sqrt(param1 ** 2 + param2 ** 2)) / 50, 1)
            XboxController.set_vibration(left_strength, right_strength)
            XboxController.vibration_user["axis_right"] = "right"
        else:
            XboxController.set_vibration(0, 0)
            XboxController.vibration_user.clear()
    elif len(XboxController.vibration_user) != 0:
        if "axis_right" in XboxController.vibration_user:
            if param1 != 0 or param2 != 0:
                left_strength = 0
                right_strength = min((math.sqrt(param1 ** 2 + param2 ** 2)) / 50, 1)
                XboxController.set_vibration(left_strength, right_strength)
            else:
                XboxController.vibration_user.clear()
    ##############################################
    ##############################################

    # -------------------------#
    # B控制姿态角还原
    # -------------------------#
    if button_state.get('B'):
        XboxController.event_vibration_feedback('back')

    # -------------------------#
    # A
    # -------------------------#
    if button_state.get('A'):
        XboxController.event_vibration_feedback('come')

    # -------------------------#
    # LB、RB挡板
    # -------------------------#
    param1 = 1 if button_state.get('LB') is True else 0
    param2 = 1 if button_state.get('RB') is True else 0
    if param1 != 0 or param2 != 0:
        XboxController.event_vibration_feedback('light')

    # -------------------------#
    # 手柄全权掌控
    # -------------------------#
    if button_state.get('task'):
        XboxController.event_vibration_feedback('switch')
    if button_state.get('X'):
        XboxController.event_vibration_feedback('fail')
    if button_state.get('Y'):
        XboxController.event_vibration_feedback('success')
    if button_state.get('settings'):
        XboxController.event_vibration_feedback('switch')


XboxController = my_xbox_handle.XboxController()
while True:
    handle_work()
    time.sleep(0.03)
