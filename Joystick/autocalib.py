import sys
import serial
import time
import serial.tools.list_ports
import re
import numpy as np
import pickle

ser = serial.Serial('/dev/ttyUSB0', 460800)
if ser. isOpen:
    print(ser.name + ' Comms open')

a=0
b=0
c=0
d=0
e=0
rng = 100
fullgrad = 400
checker = 0
sensor1 = [0,0,0,0,0]
sensor2 = [0,0,0,0,0]
sensor3 = [0,0,0,0,0]
sensor4 = [0,0,0,0,0]
sensor1avg = 0
sensor2avg = 0
sensor3avg = 0
sensor4avg = 0

setting = input('Stream?')
strmset = 'stream %s' %(setting)
nostrmset = 'stream 0'
endop = '\r\n'
strm = strmset+endop
nostrm = nostrmset+endop


testres = [0,0,0,0]

ymax = [0,100]
ymin = [0,-100]
yzero = [0,0]
yvalue = [0,0]
yavgzero = [0,0]
ygrad = 0


xmax = [0,100]
xmin = [0,-100]
xzero = [0,0]
xvalue = [0,0]
xavgzero = [0,0]
xgrad = 0

upvallist = [0]
downvallist = [0]
upvalavg = 0
downvalavg = 0

while(True):

    checker = input('Set Y ZERO')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1.append(testres[1])
        sensor2.append(testres[3])
        resp = ser.readline()

    sensor1avg = sum(sensor1)/rng
    sensor2avg = sum(sensor2)/rng

    yvalue[0] = sensor1avg - sensor2avg
    yzero[0] = yvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor1 = [0]
    sensor2 = [0]
    time.sleep(0.005)


    checker = input('Set X ZERO')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3.append(testres[1])
        sensor4.append(testres[3])

    sensor3avg = sum(sensor3)/rng
    sensor4avg = sum(sensor4)/rng

    xvalue[0] = sensor3avg - sensor4avg
    xzero[0] = xvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor3 = [0]
    sensor4 = [0]
    time.sleep(0.005)

    checker = input('Set Y MAX')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1.append(testres[1])
        sensor2.append(testres[3])
        resp = ser.readline()

    sensor1avg = sum(sensor1)/rng
    sensor2avg = sum(sensor2)/rng

    yvalue[0] = sensor1avg - sensor2avg
    ymax[0] = yvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor1 = [0]
    sensor2 = [0]
    time.sleep(0.005)

    checker = input('Set X MAX')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3.append(testres[1])
        sensor4.append(testres[3])

    sensor3avg = sum(sensor3)/rng
    sensor4avg = sum(sensor4)/rng

    xvalue[0] = sensor3avg - sensor4avg
    xmax[0] = xvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor3 = [0]
    sensor4 = [0]
    time.sleep(0.005)

    checker = input('Set Y MIN')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1.append(testres[1])
        sensor2.append(testres[3])
        resp = ser.readline()

    sensor1avg = sum(sensor1)/rng
    sensor2avg = sum(sensor2)/rng

    yvalue[0] = sensor1avg - sensor2avg
    ymin[0] = yvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor1 = [0]
    sensor2 = [0]
    time.sleep(0.005)

    checker = input('Set X MIN')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3.append(testres[1])
        sensor4.append(testres[3])

    sensor3avg = sum(sensor3)/rng
    sensor4avg = sum(sensor4)/rng

    xvalue[0] = sensor3avg - sensor4avg
    xmin[0] = xvalue[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor3 = [0]
    sensor4 = [0]
    time.sleep(0.005)

    checker = input('Calculate DEADZONE')
    ygrad = (ymax[0]-ymin[0])/fullgrad
    xgrad = (xmax[0]-xmin[0])/fullgrad
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1.append(testres[1])
        sensor2.append(testres[3])
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3.append(testres[1])
        sensor4.append(testres[3])

    sensor1avg = (sum(sensor1))/(rng)
    sensor2avg = (sum(sensor2))/(rng)
    sensor3avg = (sum(sensor3))/(rng)
    sensor4avg = (sum(sensor4))/(rng)

    yvalue[0] = sensor1avg-sensor2avg
    xvalue[0] = sensor3avg-sensor4avg

    yvalue[1] = (yvalue[0]-yzero[0])/ygrad
    xvalue[1] = (xvalue[0]-xzero[0])/xgrad

    yavgzero=yvalue[1]
    xavgzero=xvalue[1]

    ser.write(nostrm.encode())
    resp = ser.readline()

    checker = input('Find UP value')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    sensor1=[0]
    sensor2=[0]
    sensor3=[0]
    sensor4=[0]
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1 = testres[1]
        sensor2 = testres[3]
        time.sleep(0.005)
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3 = testres[1]
        sensor4 = testres[3]
        upvallist.append(sensor1+sensor2+sensor3+sensor4)

    upvalavg = sum(upvallist)/(rng)

    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor1 = [0]
    sensor2 = [0]
    sensor3 = [0]
    sensor4 = [0]
    time.sleep(0.005)

    checker = input('Find DOWN value')
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    sensor1=[0]
    sensor2=[0]
    sensor3=[0]
    sensor4=[0]
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor1 = testres[1]
        sensor2 = testres[3]
        time.sleep(0.005)
        resp = ser.readline()
        res = resp.decode()
        testres = [int(s) for s in re.findall(r'\d+', res)]
        sensor3 = testres[1]
        sensor4 = testres[3]
        downvallist.append(sensor1+sensor2+sensor3+sensor4)

    downvalavg = sum(downvallist)/(rng)

    ser.write(nostrm.encode())
    resp = ser.readline()
    sensor1 = [0]
    sensor2 = [0]
    sensor3 = [0]
    sensor4 = [0]
    time.sleep(0.005)

    file = open('calibval.txt','wb')
    memory = [ymax[0], xmax[0], ymin[0], xmin[0], yzero[0], xzero[0], ygrad, xgrad, yavgzero, xavgzero, upvalavg, downvalavg]
    memory = [round(num) for num in memory]
    print(memory)
    pickle.dump(memory,file)
    file.close()
    print('Exported!')


    e+=1


    sys.exit()
