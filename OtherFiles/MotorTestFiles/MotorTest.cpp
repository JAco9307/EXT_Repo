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

    if(argc == 1){ //if no arguments turn off and end execution
        digitalWrite(1, LOW);
        return 0;
    }

    for (EVER)
        digitalWrite(1, HIGH);
        delayMicroseconds(atoi(argv[1]));
        digitalWrite(1, LOW);
        delayMicroseconds(atoi(argv[1]));
    return 0;
}