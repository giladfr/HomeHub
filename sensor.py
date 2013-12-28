import os
import sys
import serial
import time


class Sensor(object):
    def __init__(self):
        self.ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=5)
        while not self.ser.isOpen():
            pass
        self.temp = 0
        self.humid = 0


    def update_temp_humid(self):
        self.ser.write("t\n")
        time.sleep(2)
        out = self.ser.readline()
        out_splt = out.split(",")
        print "Sensor: update temp humid response - ",out
        if out_splt[0] == "OK":
            self.temp = float(out_splt[2])
            self.humid = float(out_splt[1]) 
        

    def get_temp_humid(self):
        self.update_temp_humid()
        return (self.temp,self.humid)


