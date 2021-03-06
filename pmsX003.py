import serial
import time
import datetime
import json
import socket
import csv


sensorID = 4 # Imput a sensor number here 

# setup onboard serial port NB RPi 3 address
port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=2.0)
remote_PORT = 33333;
remote_HOST = '46.101.13.195' # IP of cloud server
csvFile="/home/pi/AirQuality/client/pm.log" # keep a local copy for debug
w = csv.writer(open(csvFile,'a'),dialect='excel')
local_PORT = 33333
local_HOST = '10.15.40.221'
# function to read a line of serial data
def read_pm_line(_port):
    rv = b''
    while True:
        ch1 = _port.read()
        if ch1 == b'\x42':
            ch2 = _port.read()
            if ch2 == b'\x4d':
                rv += ch1 + ch2
                rv += _port.read(28)
                return rv

# initalise variables
loop = 0

while True: # PMSx003 sensor by default streams data and non-uniform intervals - replace with timed polling
    try:
        print("trying to read")
        rcv = read_pm_line(port)
        print("is reading")
        
        #  The following needs updating to work on python 3
        res = {
            '_sid': sensorID, # move to static data
            '_type': 'pm', # move to static data
            '$timestamp': str(datetime.datetime.now()),
            '$PM10': ord(rcv[4]) * 256 + ord(rcv[5]),
            '$PM25_CF1': ord(rcv[6]) * 256 + ord(rcv[7]),
            '$PM100_CF1': ord(rcv[8]) * 256 + ord(rcv[9]),
            '$PM10_STD': ord(rcv[10]) * 256 + ord(rcv[11]),
            '$PM25_STD': ord(rcv[12]) * 256 + ord(rcv[13]),
            '$PM100_STD': ord(rcv[14]) * 256 + ord(rcv[15]),
            '$gr03um': ord(rcv[16]) * 256 + ord(rcv[17]),
            '$gt05um': ord(rcv[18]) * 256 + ord(rcv[19]),
            '$gr10um': ord(rcv[20]) * 256 + ord(rcv[21]),
            '$gr25um': ord(rcv[22]) * 256 + ord(rcv[23]),
            '$gr50um': ord(rcv[24]) * 256 + ord(rcv[25]),
            '$gr100um': ord(rcv[26]) * 256 + ord(rcv[27])
            }

        message = json.dumps(res)
        print(message)
        w.writerow(message)
        sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
        sock.sendto(message, (local_HOST, local_PORT))
        sock.sendto(message, (remote_HOST, remote_PORT))

        time.sleep(0.1) # wait ten millisonds

        # rcv_list.append(res.copy())
        loop += 1
    except KeyboardInterrupt:
        break
