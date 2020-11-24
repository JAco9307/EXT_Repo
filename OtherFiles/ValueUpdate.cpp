#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <stdio.h> 


int main(int argc, char* argv[])
{
    int Delta_x{ atoi(argv[1]) }, Delta_y{ atoi(argv[2]) }, Delta_z{ atoi(argv[3]) };

    int shmid;
    int* array;
    int count = 3;
    int i = 0;
    int SizeMem;
    key_t key = ftok("shmfile", 66);

    SizeMem = sizeof(*array) * count;
    shmid = shmget(key, count * sizeof(int), IPC_CREAT);
    array = (int*)shmat(shmid, 0, 0);

    array[0] = Delta_x;
    array[1] = Delta_y;
    array[2] = Delta_z;

    shmdt((void*)array);

    std::cout << "Recieved args x:" << Delta_x << ", y:" << Delta_y << ", z:" << Delta_z << std::endl;
    return 0;
}