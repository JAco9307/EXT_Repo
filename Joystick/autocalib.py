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

deadlist = [0]

upvallist = [0]
downvallist = [0]
upvalavg = 0
downvalavg = 0
polarity = 0

def ZeroFinder(box1,s1,s2,s1avg,s2avg,V,Z,checker,range):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(range):
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s1.append(box1[1])
        s2.append(box1[3])
        resp = ser.readline()

    s1avg = sum(s1)/range
    s2avg = sum(s1)/range
    V[0] = s1avg-s2avg
    Z[0] = V[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    s1 = [0]
    s2 = [0]
    time.sleep(0.005)
    return Z[0]

def YMaxMinFinder(box1,s1,s2,s1avg,s2avg,V,maxmin,checker,range):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(range):
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s1.append(box1[1])
        s2.append(box1[3])
        resp = ser.readline()

    s1avg = sum(s1)/range
    s2avg = sum(s1)/range
    V[0] = s1avg-s2avg
    maxmin[0] = V[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    s1 = [0]
    s2 = [0]
    time.sleep(0.005)
    return maxmin[0]

def XMaxMinFinder(box1,s1,s2,s1avg,s2avg,V,maxmin,checker,range):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(range):
        resp = ser.readline()
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s1.append(box1[1])
        s2.append(box1[3])

    s1avg = sum(s1)/range
    s2avg = sum(s1)/range
    V[0] = s1avg-s2avg
    maxmin[0] = V[0]
    checker = 0
    ser.write(nostrm.encode())
    resp = ser.readline()
    s1 = [0]
    s2 = [0]
    time.sleep(0.005)
    return maxmin[0]

def DeadzoneFinder(box1,s1,s2,s3,s4,s1avg,s2avg,s3avg,s4avg,YV,XV,YZ,XZ,Ygrad,Xgrad,YavgZ,XavgZ,range):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(rng):
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s1.append(box1[1])
        s2.append(box1[3])
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s3.append(box1[1])
        s4.append(box1[3])

    s1avg = (sum(s1))/(range)
    s2avg = (sum(s2))/(range)
    s3avg = (sum(s3))/(range)
    s4avg = (sum(s4))/(range)
    YV[0] = s1avg-s2avg
    XV[0] = s3avg-s4avg
    YV[1] = (YV[0]-YZ[0])/Ygrad
    XV[1] = (XV[0]-XZ[0])/Xgrad
    YavgZ = YV[1]
    XavgZ = XV[1]

    ser.write(nostrm.encode())
    resp = ser.readline()
    time.sleep(0.005)
    return [YavgZ, XavgZ]

def UpDownFinder(box1,s1,s2,s3,s4,vallist,valavg,range):
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    s1=[0]
    s2=[0]
    s3=[0]
    s4=[0]
    ser.write(strm.encode())
    resp = ser.readline()

    for x in range(range):
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s1 = box1[1]
        s2 = box1[3]
        time.sleep(0.005)
        resp = ser.readline()
        res = resp.decode()
        box1 = [int(s) for s in re.findall(r'\d+', res)]
        s3 = box1[1]
        s4 = box1[3]
        vallist.append(s1+s2+s3+s4)

    valavg = sum(vallist)/range
    ser.write(nostrm.encode())
    resp = ser.readline()
    s1 = [0]
    s2 = [0]
    s3 = [0]
    s4 = [0]
    time.sleep(0.005)
    return valavg

def JoystickPolarityFinder(up,down,pol):
    if up > down:
        polarity = 1
    elif down > up:
        polarity = 0
    return pol

while(True):

    checker = input('Set Y and X ZERO')
    yzero[0] = ZeroFinder(testres,sensor1,sensor2,sensor1avg,sensor2avg,yvalue,yzero,checker,rng)
    xzero[0] = ZeroFinder(testres, sensor3,sensor4,sensor3avg,sensor4avg,xvalue,xzero,checker,rng)

    checker = input('Set Y MAX')
    ymax[0] = YMaxMinFinder(testres,sensor1,sensor2,sensor1avg,sensor2avg,yvalue,ymax,checker,rng)

    checker = input('Set X MAX')
    xmax[0] = XMaxMinFinder(testres,sensor3,sensor4,sensor3avg,sensor4avg,xvalue,xmax,checker,rng)

    checker = input('Set Y MIN')
    ymin[0] = YMaxMinFinder(testres,sensor1,sensor2,sensor1avg,sensor2avg,yvalue,ymin,checker,rng)

    checker = input('Set X MIN')
    xmin[0] = XMaxMinFinder(testres,sensor3,sensor4,sensor3avg,sensor4avg,xvalue,xmin,checker,rng)

    ygrad = (ymax[0]-ymin[0])/fullgrad
    xgrad = (xmax[0]-xmin[0])/fullgrad

    checker = input('Calculate DEADZONE')
    deadlist = DeadzoneFinder(testres,sensor1,sensor2,sensor3,sensor4,sensor1avg,sensor2avg,sensor3avg,sensor4avg,yvalue,xvalue,yzero,xzero,ygrad,xgrad,yavgzero,xavgzero,rng)
    yavgzero = deadlist[0]
    xavgzero = deadlist[1]

    checker = input('Find UP value')
    upvalavg = UpDownFinder(testres,sensor1,sensor2,sensor3,sensor4,upvallist,upvalavg,rng)

    checker = input('Find DOWN value')
    downvalavg = UpDownFinder(testres,sensor1,sensor2,sensor3,sensor4,downvallist,downvalavg,rng)
    polarity = JoystickPolarityFinder(upvalavg,downvalavg,polarity)

    file = open('calibval.txt','wb')
    memory = [ymax[0], xmax[0], ymin[0], xmin[0], yzero[0], xzero[0], ygrad, xgrad, yavgzero, xavgzero, upvalavg, downvalavg, polarity]
    memory = [round(num) for num in memory]
    print(memory)
    pickle.dump(memory,file)
    file.close()
    print('Exported!')


    e+=1


    sys.exit()
