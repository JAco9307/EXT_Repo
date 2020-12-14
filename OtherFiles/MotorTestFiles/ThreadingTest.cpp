#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <stdio.h> 
#include <fstream>
#include <stdlib.h>
#include <thread>
#include <wiringPi.h>
#include <ncurses.h>

using namespace std;

#define Motor1Pol 1
#define Motor1Dir 16

#define Motor2Pol 23
#define Motor2Dir 22

#define EVER ;;

int dirx = 0, diry = 0;
int delpointing1, delpointing2;
static int* del1 = &delpointing1;
static int* del2 = &delpointing2;

void MotorThread(int Motor, int* Delay);



void ThreadTest(int* i);


int main(int argc, char* argv[])
{
    wiringPiSetup();
    pinMode(Motor1Pol,OUTPUT);
    pinMode(Motor1Dir,OUTPUT);
    pinMode(Motor2Pol,OUTPUT);
    pinMode(Motor2Dir,OUTPUT);
    *del1 = atoi(argv[1]);
    *del2 = atoi(argv[2]);
    thread Motor1(MotorThread, Motor1Pol, &dirx); //Motor1 thread 
    thread Motor2(MotorThread, Motor2Pol, &diry); //Motor1 thread 
    initscr(); //remember about errors support
    

    while(1){
        int c = getchar();
        switch(c) {
        case 65:
            dirx = 1;
            digitalWrite(Motor1Dir, LOW);
            break;
        case 66:
            dirx = 1;
            digitalWrite(Motor1Dir, HIGH);
            break;
        case 67:
            diry = 1;
            digitalWrite(Motor2Dir, LOW);
            break;
        case 68:
            diry = 1;
            digitalWrite(Motor2Dir, HIGH);
            break;
        
        case '\r':
            diry=0;
            dirx=0;
            cout << "Enter" << endl;
            break;
        }
        //cout << "\rdirx: " << dirx << " diry: " << diry << flush;
    }
    return 0;
}


void MotorThread(int Motor, int* Delay){
    for(EVER){
        if(*Delay != 0 ){
            int OnDelay = *del1;
            int OffDelay = *del2;
            digitalWrite(Motor, HIGH);
            delayMicroseconds(OnDelay);
            digitalWrite(Motor, LOW);
            delayMicroseconds(OffDelay);
        }
        else delayMicroseconds(10000);
    }
}