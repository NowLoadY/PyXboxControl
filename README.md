# PyXboxControl
![](https://img.shields.io/badge/python-3.x-brightgreen)

<img src="https://github.com/NowLoadY/PyXboxControl/blob/main/img/pyxboxcontrol.jpg" alt="pyxboxcontrol" width="400px" />
(not official but easy to use)

PyXboxControl is a Python library for controlling an Xbox controller. It provides a simple interface for capturing joystick and button inputs and applying force feedback to the controller.

## Usage

Here's a simple example of how to use PyXboxControl:

```python
# you can simply run the code for test.
import pyxboxcontrol
import time

xbox = pyxboxcontrol.XboxController()

while True:
    # get info
    joystick_state, button_state = xbox.get_joystick_state()
    print(joystick_state)
    # print(button_state)
    
    # apply force feedback
    left_strength = joystick_state.get('LT')/100
    right_strength = joystick_state.get('RT')/100
    xbox.set_vibration(left_strength, right_strength)

    if button_state.get('B'):
        xbox.event_vibration_feedback('back')
    if button_state.get('X'):
        xbox.event_vibration_feedback('fail')
    if button_state.get('Y'):
        xbox.event_vibration_feedback('success')
    time.sleep(0.03)
```

You can use the XboxController class to capture inputs from the controller and apply force feedback.

## Contributing

You're welcome to contribute to PyXboxControl! 

## License

PyXboxControl is released under the MIT License. See the LICENSE file for more information.

## Acknowledgments

PyXboxControl refer to the [Xbox-Controller-for-Python](https://github.com/r4dian/Xbox-Controller-for-Python) library by r4dian and rely on pygame. 
