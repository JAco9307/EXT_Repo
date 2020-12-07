#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <stdio.h> 
#include <wiringPi.h>
using namespace std;

int main(int argc, char* argv[])
{
    wiringPiSetup();
    pinMode(0,OUTPUT);
    digitalWrite(0, atoi(argv[1])); //works
    return 0;
}