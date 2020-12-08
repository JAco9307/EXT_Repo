#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <stdio.h> 
#include <wiringPi.h>
using namespace std;
#define EVER ;;

int main(int argc, char* argv[])
{
    wiringPiSetup();
    pinMode(1,OUTPUT);
    pinMode(16,OUTPUT);

    if(argc == 1){ //if no arguments turn off and end execution
        digitalWrite(1, LOW);
        return 0;
    }

    int i = 0, d = 0, dir = 0;
    for (EVER)
    {   
        i++;
        if(i == 225){
            i=0; 
            d++;
        }
        digitalWrite(1, HIGH);
        delayMicroseconds(atoi(argv[1]));
        digitalWrite(1, LOW);
        delayMicroseconds(atoi(argv[1]));
        cout << "\r" << "Rotations: " << d << flush;
    }
    return 0;
}