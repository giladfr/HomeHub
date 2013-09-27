__author__ = 'giladfride'

import serial
import time


CMD_OP = 0xFF
CMD_CLEAR = 0x0A
CMD_BACKLIGHT_OFF = 0xB
CMD_BACKLIGHT_ON = 0xC
CMD_SET_CURSOR = 0xD


class LCDLine(object):
    def __init__(self,num = 0,width = 16):
        self.width = width
        self.str = " " * width

class LCD(object):
    def __init__(self,comport,n_lines = 2,n_col = 16):
        self.n_lines = n_lines
        self.n_col = n_col
        self.ser = serial.Serial(port=comport, baudrate=9600, bytesize=serial.EIGHTBITS,\
                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        self.cur_lines = []
        self.next_lines = []
        for i in range(1,self.n_lines):
            self.cur_lines.append(LCDLine())
            self.next_lines.append(LCDLine())

        time.sleep(1)



    def write(self,str):
        self.ser.write(str)

    def clear(self):
        self._cmd(CMD_CLEAR)

    def set_backlight(self,state):
        if state:
            self._cmd(CMD_BACKLIGHT_ON)
        else:
            self._cmd(CMD_BACKLIGHT_OFF)

    def set_cursor(self,col,row):
        self.ser.write(chr(CMD_OP) + chr(CMD_SET_CURSOR) + chr(col) + chr(row))

    def add_timestamp(self):
        self.set_cursor(0,0)
        self.write(time.strftime(" %d/%m %H:%M:%S", time.localtime()))
        self.set_cursor(0,1)



    def _cmd(self,cmd):
        self.ser.write(chr(CMD_OP) + chr(cmd))

