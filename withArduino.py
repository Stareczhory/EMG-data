import serial
import datetime

def readserial(comport, baudrate):
    ser = serial.Serial(comport, baudrate, timeout=0.01)

    while True:
        data = ser.readline().decode().strip()
        if data:
            current_time = datetime.datetime.now()
            print(data, current_time)


readserial('COM4', 9600)