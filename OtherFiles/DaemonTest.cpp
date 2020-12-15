#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <wiringPi.h>
#include <thread>

using namespace std;
#define EVER ;;

#define Motor1Pol 1
#define Motor1En 8
#define Motor1Dir 16

#define Motor2Pol 23
#define Motor2En 9
#define Motor2Dir 22

int Delay1 = 0, Delay2 = 0;
int dirx = -1, diry = -1;

void InitPins(void);
void DefaultMemory(void);
void MotorControl(int const (&JoystPos)[3], int (&CranePos)[3]);
void SetMotor(int const &Pos, int &Dir, int &Delay);
void CopyMemory(int (&JoystPos)[3], int* const Recieve);
void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]);
void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]);

void MotorThread(int Motor, int enable, int MotorDir, int RangeTop, int RangeBot, int* Steps, int* dir, int* delay);

int main() {
    DefaultMemory(); //initializes memory to zero in case previous non zero persist
    wiringPiSetup(); //Initializes pin usage
    InitPins();      //Initializes used pins
    
    //Initialize variables
    int* Recieve;
    int JoystPos[3] = { 0, 0, 0 };
    int CranePos[3] = { 0, 0, 0 };

    //Direct pointer to shared memory with readonly access
    key_t key = ftok("shmfile", 66);
    int shmid = shmget(key, 3 * sizeof(int), IPC_EXCL);
    Recieve = (int*)shmat(shmid, (void*)0, SHM_RDONLY);

    thread Motor1(MotorThread, Motor1Pol, Motor1En, Motor1Dir, 4000, 0, &(CranePos[0]), &dirx, &Delay1); //Motor1 thread 
    thread Motor2(MotorThread, Motor2Pol, Motor2En, Motor2Dir, 2800, 0, &(CranePos[1]), &diry, &Delay2);
	
    for (EVER)
    {
        //Copy data to local variable, to avoid data changing mid execution
        CopyMemory(JoystPos, Recieve);

        WriteToFile(JoystPos,CranePos);//Writes posistions to file for the webserver

        MotorControl(JoystPos,CranePos); //All motor control in here

        DumpVal(JoystPos,CranePos); //Dumps values to cout for debugging

        delayMicroseconds(5000);
    }

    shmdt((void*)Recieve);

    return 0;
}

void InitPins(void){
    //motor control output:
    pinMode(Motor1Pol,OUTPUT);
    pinMode(Motor1Dir,OUTPUT);
    pinMode(Motor2Pol,OUTPUT);
    pinMode(Motor2Dir,OUTPUT);
    pinMode(Motor1En,OUTPUT);
    pinMode(Motor2En,OUTPUT);
    //endswitch reads:

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
    array = 0, 0, 0;

    shmdt((void*)array);
}

void CopyMemory(int (&JoystPos)[3], int* const Recieve){
    JoystPos[0] = Recieve[0];
    JoystPos[1] = Recieve[1];
    JoystPos[2] = Recieve[2];
}


void MotorControl(int const (&JoystPos)[3], int (&CranePos)[3]){
    SetMotor(JoystPos[0], dirx, Delay1);
    SetMotor(JoystPos[1], diry, Delay2);
} 

void SetMotor(int const &Pos, int &Dir, int &Delay)
{
    if (Pos == 0){
        Dir = -1;
    }
    else {
        if (Pos < 0){
            Dir = 0;
        }
        else{
            Dir = 1;
        }
        Delay = (8*(250-Pos)+200);
    }
}

void TakeStep(int enable, int motor, int delay){
    digitalWrite(enable, LOW);
    digitalWrite(motor, HIGH);
    delayMicroseconds(delay/4);
    digitalWrite(motor, LOW);
    delayMicroseconds(delay);
}

void MotorThread(int Motor, int enable, int MotorDir, int RangeTop, int RangeBot, int* Steps, int* dir, int* delay){
    for(EVER){
        if(*dir == 1){
            digitalWrite(MotorDir, HIGH);
            if (++(*Steps) >= RangeTop)
            {
                *Steps =  RangeTop;
                digitalWrite(enable, HIGH);
            }
            else{
                TakeStep(enable, Motor, *delay);
            }
        } else if(*dir == 0){
            digitalWrite(MotorDir, LOW);
            if (--(*Steps) <= RangeBot)
            {
                *Steps =  RangeBot;
                digitalWrite(enable, HIGH);
            }
            else{
                TakeStep(enable, Motor, *delay);
            }
        } else digitalWrite(enable, HIGH);  
    }
}

void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]){
    cout << "\r";
    cout << "x:" << JoystPos[0] << ", y:" << JoystPos[1] << ", z:" << JoystPos[2];
    cout << " | xp:" << CranePos[0] << ", yp:" << CranePos[1] << ", zp:" << CranePos[2];
    cout << " | Delay1: " << Delay1 << " Delau2: " << Delay2 << flush;
}

void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]){  
    std::ofstream ofs;
    ofs.open("../htdocs/CranePos.txt", std::ofstream::out | std::ofstream::trunc);
    ofs << JoystPos[0] << ',' << JoystPos[1] << ',' << JoystPos[2] << ';' << CranePos[0]/200 << ',' << CranePos[1]/200 << ',' << CranePos[2];
    ofs.close();
}