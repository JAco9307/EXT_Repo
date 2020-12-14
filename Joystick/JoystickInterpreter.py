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
polarity = 0
total = 0
zout = 0

def StreamReader(box1,s1,s2,V,Z,grad,dead,out,deadzone):
    resp = ser.readline()
    res = resp.decode()
    #this line takes only the integers from the stream response
    box1 = [int(s) for s in re.findall(r'\d+', res)]
    s1 = box1[1]
    s2 = box1[3]
    V[0] = s1-s2
    V[1] = (V[0]-Z[0])/grad
    #Dead zone and upper limit calculation
    if V[1] > (dead+deadzone) or V[1] < (dead-deadzone):
        if V[1] > 200:
            out = 200
            print(out)
        elif V[1] < -200:
            out = -200
            print(out)
        else:
            out = int(V[1])
            print(out)
    else:
        out = 0
        print(out)

    return out

def UpDown(yO,xO,upval,downval,zO,s1,s2,s3,s4):
    if yO == 0 and xO == 0:
        total = s1+s2+s3+s4
        if polarity == 1:
            if total >= (upval):
                zO = 1
                print('UP')
            elif total =< (downval):
                zO = -1
                print('DOWN')
            else:
                zO = 0
        elif polarity == 0:
            if total =< (upval):
                zO = 1
                print('UP')
            elif total >= (downval):
                zO = -1
                print('DOWN')
            else:
                zO = 0
    return zO

while(True):
    try:
        if a <= 0:
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
            polarity = vals[12]
            a+=1
            time.sleep(0.005)

        else:
            #Y axis Processing
            yout = StreamReader(testres,sensor1,sensor2,yvalue,yzero,ygrad,ydead,yout,deadZ)
            #X axis Processing
            xout = StreamReader(testres,sensor3,sensor4,xvalue,xzero,xgrad,xdead,xout,deadZ)
            #updown processing
            zout = UpDown(yout,xout,upvalavg,downvalavg,zout,sensor1,sensor2,sensor3,sensor4)
            #sending to the controller
            os.system("CLI " + str(xout) + " " + str(yout) + " " + str(int(zout)))
            time.sleep(0.005)

    except KeyboardInterrupt:
        os.system("CLI")
        ser.write(nostrm.encode())
        resp = ser.readline()
        print("\n *** Exit Seq *** \n")
        sys.exit()
