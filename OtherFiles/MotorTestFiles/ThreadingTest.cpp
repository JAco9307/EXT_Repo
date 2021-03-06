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
#define Motor1En 8
#define Motor1Dir 16

#define Motor2Pol 23
#define Motor2En 9
#define Motor2Dir 22

#define DC1 24
#define DC2 25

#define EndSwx 29
#define EndSwy 28
#define EndSwz 27

#define EVER ;;

int dirx = -1, diry = -1;
int del1 = 0;
int stepxp = 0, stepyp = 0;
//static int* del1 = &delpointing1;
//static int* del2 = &delpointing2;


//void MotorThread(int Motor, int enable, int MotorDir, int RangeTop, int RangeBot, int* Steps, int* dir);

void PinSetup(void);


int main(int argc, char* argv[])
{
    wiringPiSetup();
    PinSetup();
    //del1 = atoi(argv[1]);
    //thread Motor1(MotorThread, Motor1Pol, Motor1En, Motor1Dir, 4000, 0, &stepxp, &dirx); //Motor1 thread 
    //thread Motor2(MotorThread, Motor2Pol, Motor2En, Motor2Dir, 2800, 0, &stepyp, &diry); //Motor1 thread 
    //initscr(); //getchar setup ?
    
    while(1){
        delayMicroseconds(50000);
        cout << digitalRead(EndSwx) << " " << digitalRead(EndSwy) << " " << digitalRead(EndSwz) << endl;
        /*int c = getchar();
        switch(c) {
        case 65:
            dirx = 1;
            
            break;
        case 66:
            dirx = 0;
            
            break;
        case 67:
            diry = 1;
            
            break;
        case 68:
            diry = 0;
            
            break;
        case '\r':            
            dirx = -1;
            diry = -1;
            break;
        }
        cout << "\rStepx: " << stepxp << " stepy: " << stepyp << endl;
        cout << "\rDirx: " << dirx << " Diry: " << diry << endl;*/
    }
    return 0;
}

void TakeStep(int enable, int motor){
    digitalWrite(enable, LOW);
    digitalWrite(motor, HIGH);
    delayMicroseconds(del1/4);
    digitalWrite(motor, LOW);
    delayMicroseconds(del1);
}

void MotorThread(int Motor, int enable, int MotorDir, int RangeTop, int RangeBot, int* Steps, int* dir){
    for(EVER){
        if(*dir == 1){
            digitalWrite(MotorDir, HIGH);
            if (++(*Steps) >= RangeTop)
            {
                *Steps =  RangeTop;
                digitalWrite(enable, HIGH);
            }
            else{
                TakeStep(enable, Motor);
            }
        } else if(*dir == 0){
            digitalWrite(MotorDir, LOW);
            if (--(*Steps) <= RangeBot)
            {
                *Steps =  RangeBot;
                digitalWrite(enable, HIGH);
            }
            else{
                TakeStep(enable, Motor);
            }
        } else digitalWrite(enable, HIGH);  
    }
}

void PinSetup(void){
    pinMode(Motor1Pol,OUTPUT);
    pinMode(Motor1Dir,OUTPUT);
    pinMode(Motor2Pol,OUTPUT);
    pinMode(Motor2Dir,OUTPUT);
    pinMode(Motor1En,OUTPUT);
    pinMode(Motor2En,OUTPUT);
    pinMode(DC1,OUTPUT);
    pinMode(DC2,OUTPUT);
    pinMode(EndSwx,INPUT);
    pinMode(EndSwy,INPUT);
    pinMode(EndSwz,INPUT);

    digitalWrite(DC1, LOW);
}