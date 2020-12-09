#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <stdio.h> 
#include <thread> 
#include <fstream>
#include <stdlib.h>
#include <wiringPi.h>
using namespace std;

#define EVER ;;


void ThreadTest(void);
int i;
std::thread thread_object(ThreadTest);

int main(int argc, char* argv[])
{
    thread t1(ThreadTest);
    while(1){
        delayMicroseconds(500000);
        i++;
    }

    return 0;
}

void ThreadTest(void){
    for(EVER){
        cout << "\rthread access: " << i << flush;
        delayMicroseconds(50000);
    }
}