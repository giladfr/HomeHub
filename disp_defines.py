__author__ = 'giladfride'

import sys

# General configuration
DISP_SERVER_PORT = 50000 # display server listen port
MAX_MSG_LEN = 32

# configuration of the serial port that the display is connected to
if sys.platform == "darwin":
    CONNECTED_DISPLAYS = ["/dev/tty.usbserial-A7005O9s"]
elif sys.platform.startswith("Linux"):
    CONNECTED_DISPLAYS = ["/dev/ttyUSB0"]



