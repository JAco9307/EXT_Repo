import serial
import time
import serial.tools.list_ports
import re
import numpy as np
import pickle
import os, sys

ser = serial.Serial('/dev/ttyUSB0', 460800)
if ser. isOpen:
    print(ser.name + ' Comms open')


a=0
sensor1 = 0
sensor2 = 0
sensor3 = 0
sensor4 = 0

sensor1prev = 0
sensor2prev = 0
sensor3prev = 0
sensor4prev = 0

setting = input("Stream? ")
strmset = 'stream %s' %(setting)
nostrmset = 'stream 0'
endop = '\r\n'
strm = strmset+endop
nostrm = nostrmset+endop
ser.write(strm.encode())


testres = [10, 10, 10,10]

ymax = [0,100]
ymin = [0,-100]
yzero = [0,0]
yvalue = [0,0]
ygrad = 0


xmax = [0,100]
xmin = [0,-100]
xzero = [0,0]
xvalue = [0,0]
xgrad = 0

ydead = 0
xdead = 0
deadZ = 50

yout = 0
xout = 0

upvalavg = 0
downvalavg = 0
total = 0
zout = 0

yread = [0,0,0]
xread = [0,0,0]

def StreamReader(box1,s1,s2,s1prev,s2prev,V,Z,grad,dead,out,deadzone):
    resp = ser.readline()
    res = resp.decode()
    #this line takes only the integers from the stream response
    box1 = [int(s) for s in re.findall(r'\d+', res)]
    try:
        s1 = box1[1]
    except:
        s1 = s1prev
        print('catch!')
    try:
        s2 = box1[3]
    except:
        s2 = s2prev
        print('catch!')
    V[0] = s1-s2
    V[1] = (V[0]-Z[0])/grad
    #Dead zone and upper limit calculation
    if V[1] > (dead+deadzone) or V[1] < (dead-deadzone):
        if V[1] > 200:
            out = 200
        elif V[1] < -200:
            out = -200
        else:
            out = int(V[1])
    else:
        out = 0
    s1prev = s1
    s2prev = s2
    return [out,s1prev,s2prev]

def UpDown(yO,xO,upval,downval,zO,s1,s2,s3,s4):
    if yO == 0 and xO == 0:
        total = s1+s2+s3+s4
        if (upval-total) < 0:
            zO = 1
            print('down')
        else:
            zO = 0
            print('up')
    return zO

while(True):
    try:
        if a <=0:
            #initial setup. cleaning buffers, reading STREAM confirmation, accepting values from autocalibrator
            ser.reset_output_buffer()
            ser.reset_input_buffer()
            con=ser.readline()
            con = con.decode()
            print(con)
            vals = pickle.load(open('calibval.txt', 'rb'))
            ymax[0] = vals[0]
            xmax[0] = vals[1]
            ymin[0] = vals[2]
            xmin[0] = vals[3]
            yzero[0] = vals[4]
            xzero[0] = vals[5]
            ygrad = vals[6]
            xgrad = vals[7]
            ydead = vals[8]
            xdead = vals[9]
            upvalavg = vals[10]
            downvalavg = vals[11]
            a+=1
            time.sleep(0.05)

        else:
            #Y axis Processing
            yread = StreamReader(testres,sensor1,sensor2,sensor1prev,sensor2prev,yvalue,yzero,ygrad,ydead,yout,deadZ)
            yout = yread[0]
            sensor1prev = yread[1]
            sensor2prev = yread[2]
            #X axis Processing
            xread = StreamReader(testres,sensor3,sensor4,sensor3prev,sensor4prev,xvalue,xzero,xgrad,xdead,xout,deadZ)
            xout = yread[0]
            sensor3prev = yread[1]
            sensor4prev = yread[2]
            #updown processing
            zout=UpDown(yout,xout,upvalavg,downvalavg,zout,sensor1,sensor2,sensor3,sensor4)
            #sending to the controller
            os.system("CLI " + str(xout) + " " + str(yout) + " " + str(int(zout)))
            time.sleep(0.05)

    except KeyboardInterrupt:
        os.system("CLI")
        ser.write(nostrm.encode())
        resp = ser.readline()
        print("\n *** Exit Seq *** \n")
        sys.exit()
