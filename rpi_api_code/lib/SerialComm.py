import serial

class SerialComm:
    
    def __init__(self,serialport='/dev/ttyUSB0',baudrate=9600):
        self.serialport = serialport
        self.baudrate = baudrate

    def write(self,content):
        with serial.Serial(self.serialport,self.baudrate,timeout=1) as serialdevice:
            serialdevice.write(content)
