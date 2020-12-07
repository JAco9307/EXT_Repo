#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
using namespace std;
#define EVER ;;

void DefaultMemory(void);
void MotorControl(int const (&JoystPos)[3], int (&CranePos)[3]);
void CopyMemory(int (&JoystPos)[3], int* const Recieve);
void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]);
void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]);

int main() {
    //initializes memory to zero in case previous non zero persist
    DefaultMemory(); 
    
    //Initialize variables
    int* Recieve;
    int JoystPos[3] = { 0, 0, 0 };
    int CranePos[3] = { 0, 0, 0 };

    //Direct pointer to shared memory with readonly access
    key_t key = ftok("shmfile", 66);
    int shmid = shmget(key, 3 * sizeof(int), IPC_EXCL);
    Recieve = (int*)shmat(shmid, (void*)0, SHM_RDONLY);
	
    for (EVER)
    {
        //Copy data to local variable, to avoid data changing mid execution
        CopyMemory(JoystPos, Recieve);

        MotorControl(JoystPos,CranePos); //All motor control in here

        DumpVal(JoystPos,CranePos); //Dumps values to cout for debugging

        WriteToFile(JoystPos,CranePos);//Writes posistions to file for the webserver

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

    shmid = shmget(key, count * sizeof(int), IPC_CREAT | 0660);
	if (shmid == -1) {
		perror("Could not get shared memory");
	}
    array = (int*)shmat(shmid, 0, 0);
	if (array == reinterpret_cast<void*>(-1)) {
		perror("Could not get shared memory location");
	}
    array[0] = 0;
    array[1] = 0;
    array[2] = 0;

    shmdt((void*)array);
}

void CopyMemory(int (&JoystPos)[3], int* const Recieve){
    JoystPos[0] = Recieve[0];
    JoystPos[1] = Recieve[1];
    JoystPos[2] = Recieve[2];
}


void MotorControl(int const (&JoystPos)[3], int (&CranePos)[3]){
    int i = 3;
    while(i-->0){
        if(CranePos[i] + JoystPos[i] > 20000) CranePos[i] = 20000;
        else if(CranePos[i] + JoystPos[i] < 0) CranePos[i] = 0;
        else CranePos[i] += JoystPos[i];
    }
} 

void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]){
    cout << "\r";
    cout << "x:" << JoystPos[0] << ", y:" << JoystPos[1] << ", z:" << JoystPos[2];
    cout << "| xp:" << CranePos[0] << ", yp:" << CranePos[1] << ", zp:" << CranePos[2] << flush;
}

void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]){  
    std::ofstream ofs;
    ofs.open("../htdocs/CranePos.txt", std::ofstream::out | std::ofstream::trunc);
    ofs << JoystPos[0] << ',' << JoystPos[1] << ',' << JoystPos[2] << ';' << CranePos[0]/20 << ',' << CranePos[1]/20 << ',' << CranePos[2]/20;
    ofs.close();
}