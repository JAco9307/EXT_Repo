#include <iostream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 

#define EVER ;;

void DefaultMemory(void);

int main() {

    DefaultMemory();

    int* Recieve;
    int x{ 0 }, y{ 0 }, z{0};

    key_t key = ftok("shmfile", 66);
    int shmid = shmget(key, 3 * sizeof(int), IPC_EXCL);
    Recieve = (int*)shmat(shmid, (void*)0, SHM_RDONLY);
    for (EVER)
    {
        x = Recieve[0];
        y = Recieve[1];
        z = Recieve[2];
        std::cout << "x:" << x << ", y:" << y << ", z:" << z << std::endl;
        usleep(50000);
    }

    shmdt((void*)Recieve);

    return 0;
}

void DefaultMemory() {
    int shmid;
    int* array;
    int count = 3;
    key_t key = ftok("shmfile", 66);

    shmid = shmget(key, count * sizeof(int), IPC_CREAT);
    array = (int*)shmat(shmid, 0, 0);

    array[0] = 0;
    array[1] = 0;
    array[2] = 0;

    shmdt((void*)array);
}