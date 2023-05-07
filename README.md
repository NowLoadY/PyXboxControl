# PyXboxControl(not official)

PyXboxControl is a Python library for controlling an Xbox controller. It provides a simple interface for capturing joystick and button inputs and applying force feedback to the controller.

## Usage

Here's a simple example of how to use XboxControl:

```python
import pyxboxcontrol
from xboxcontrol import XboxController

xbox = XboxController()

def handle_input(joystick, buttons):
    # Handle joystick and button input here

xbox.set_input_callback(handle_input)
xbox.start()
```

You can use the XboxController class to capture inputs from the controller and apply force feedback. See the documentation for a full list of available functions.

## Contributing

You're welcome to contribute to PyXboxControl! Here are some ways you can help:

- Submit bug reports or feature requests
- Write code or documentation
- Review open pull requests

## License

PyXboxControl is released under the MIT License. See the LICENSE file for more information.

## Acknowledgments

PyXboxControl conferrence the [Xbox-Controller-for-Python](https://github.com/r4dian/Xbox-Controller-for-Python) library by r4dian and rely on pygame. 
