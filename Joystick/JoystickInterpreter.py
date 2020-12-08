
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
b=0
c=0
d=0
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
total = 0
zout = 0

while(True):
    try:
        if b <=0:
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

            b+=1
            time.sleep(0.005)

        else:
            #main body
            resp = ser.readline()
            res = resp.decode()
            #this line takes only the integers from the stream response
            testres = [int(s) for s in re.findall(r'\d+', res)]
            sensor1 = testres[1]
            sensor2 = testres[3]
            
            yvalue[0] = sensor1-sensor2
            yvalue[1] = (yvalue[0]-yzero[0])/ygrad

            #Y axis deadzone calculation
            if yvalue[1] > (ydead+deadZ) or yvalue[1] < (ydead-deadZ):
                if yvalue[1] > 200:
                    yout = 200
                    print(yout)
                else:
                    yout = int(yvalue[1])
                    print(yout)
            else:
                yout = 0
                print(yout)

            #X axis processing
            resp = ser.readline()
            res = resp.decode()
            testres =[int(s) for s in re.findall(r'\d+', res)]
            sensor3 = testres[1]
            sensor4 = testres[3]

            xvalue[0] = sensor3-sensor4
            xvalue[1] = (xvalue[0]-xzero[0])/xgrad
            #X axis deadzone calculation
            if xvalue[1] > (xdead+deadZ) or xvalue[1] < (xdead-deadZ):
                if xvalue[1] > 200:
                    xout = 200
                    print(xout)
                else:
                    xout = int(xvalue[1])
                    print(xout)
            else:
                
                xout = 0
                print(xout)


            #updown processing    
            if yout == 0 and xout == 0:
                total = sensor1+sensor2+sensor3+sensor4
                if total >= (0.75*upvalavg):
                    zout = 1
                    print('UP')
                elif total <= (1.25*downvalavg):
                    zout = -1
                    print('DOWN')
                else:
                    zout= 0
                    
            os.system("CLI " + str(int(xout)) + " " + str(int(yout)) + " " + str(int(zout)))
            time.sleep(0.005)
    except KeyboardInterrupt:
        os.system("CLI")
        ser.write(nostrm.encode())
        resp = ser.readline()
        print("\n *** Exit Seq *** \n")
        sys.exit()
            

       

    
    
    
