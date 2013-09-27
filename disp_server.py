#!/usr/bin/env python
__author__ = 'giladfride'
DEBUG_PRINTS = True


import socket
import disp_defines
from LCD import LCD
import time



class HomeHub(object):
    def __init__(self):
        self.lcd = LCD(disp_defines.CONNECTED_DISPLAYS[0])
        time.sleep(1)
        self.lcd.clear()
        self.lcd.write("Connected...")
        self.host = ''
        self.port = disp_defines.DISP_SERVER_PORT
        self.backlog = 5
        self.size = 1024

    def main_loop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(self.backlog)
        print "Listening on port " + str(self.port)
        while 1:
            client, address = s.accept()
            data = client.recv(self.size)
            if data:
                #client.send(data)
                if DEBUG_PRINTS: print data
                self.exec_command(data)


        client.close()


    def exec_command(self,data):
        eval("self." + data)

    def disp_msg(self,msg,**kwargs):
        self.lcd.clear()
        self.lcd.add_timestamp()
        self.lcd.write(msg)


def main():
    hub_server = HomeHub()
    hub_server.main_loop()




if __name__ == "__main__":
    main()




