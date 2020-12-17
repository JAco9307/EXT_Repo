#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h> 
#include <wiringPi.h>
#include <thread>

using namespace std;
#define EVER ;;

#define Motor1Pol 23
#define Motor1En 9
#define Motor1Dir 22

#define Motor2Pol 1
#define Motor2En 8
#define Motor2Dir 16

#define EndSwx 29
#define EndSwy 28
#define EndSwz 27

int Delay1 = 1800, Delay2 = 1800;
int dirx = -1, diry = -1;

void InitPins(void);
void DefaultMemory(void);
void MotorControl(int const (&JoystPos)[3], int (&CranePos)[3]);
void SetMotor(int const &Pos, int &Dir, int &Delay);
void CopyMemory(int (&JoystPos)[3], int* const Recieve);
void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]);
void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]);

void MotorThread(int Motor, int enable, int MotorDir, int Range, int EndSw, int* Steps, int* dir, int* delay);

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

    thread Motor1(MotorThread, Motor1Pol, Motor1En, Motor1Dir, 4000, EndSwx, &(CranePos[0]), &dirx, &Delay1); //Motor1 thread 
    thread Motor2(MotorThread, Motor2Pol, Motor2En, Motor2Dir, 2800, EndSwy, &(CranePos[1]), &diry, &Delay2);
	
    int consec = 0;
    for(EVER){
        if (digitalRead(EndSwx) && digitalRead(EndSwy)){
            consec++;
        }else if (consec>=0) consec--;
        if (consec > 10) break;
        MotorControl({-200, -200, 0}, CranePos);
        DumpVal(JoystPos,CranePos);
         delayMicroseconds(5000);
    }
    MotorControl({0,0,0}, CranePos);

    for (EVER)
    {
        //Copy data to local variable, to avoid data changing mid execution
        CopyMemory(JoystPos, Recieve);

        WriteToFile(JoystPos,CranePos);//Writes posistions to file for the webserver

        MotorControl(JoystPos,CranePos); //All motor control in here

        DumpVal(JoystPos,CranePos); //Dumps values to cout for debugging

        delayMicroseconds(1000);
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
    pinMode(EndSwx,INPUT);
    pinMode(EndSwy,INPUT);
    pinMode(EndSwz,INPUT);
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
        Delay = 1800;
    }
    else {
        if (Pos < 0){
            if (Dir == 1){
                Delay = 1800;
            }
            Dir = 0;
        }
        else{
            if (Dir == 0){
                Delay = 1800;
            }
            Dir = 1;
        }
        int TargetDelay = (8*(250-abs(Pos))+200);
        if (TargetDelay < Delay-10) Delay -= 10;
        else if (TargetDelay < Delay) Delay--;
        else if (TargetDelay > Delay+10) Delay += 10;
        else if (TargetDelay > Delay) Delay++;
    }
}

void TakeStep(int enable, int motor, int delay){
    digitalWrite(enable, LOW);
    digitalWrite(motor, HIGH);
    delayMicroseconds(delay/4);
    digitalWrite(motor, LOW);
    delayMicroseconds(delay);
}

void MotorThread(int Motor, int enable, int MotorDir, int Range, int EndSw, int* Steps, int* dir, int* delay){
    for(EVER){
        if(*dir == 1){
            digitalWrite(MotorDir, HIGH);
            if (++(*Steps) >= Range)
            {
                *Steps =  Range;
                digitalWrite(enable, HIGH);
                delayMicroseconds(5000);
            }
            else{
                TakeStep(enable, Motor, *delay);
            }
        } else if(*dir == 0){
            digitalWrite(MotorDir, LOW);
            if (digitalRead(EndSw)){
                *Steps = 0;
                digitalWrite(enable, HIGH);
                delayMicroseconds(5000);
            }
            else{
                (*Steps)--;
                TakeStep(enable, Motor, *delay);
            }
        } else {
            digitalWrite(enable, HIGH);  
            delayMicroseconds(5000);
        }
    }
}

void DumpVal(int const (&JoystPos)[3], int const (&CranePos)[3]){
    cout << "x:" << JoystPos[0] << ",\t y:" << JoystPos[1] << ",\t z:" << JoystPos[2];
    cout << "\t | xp:" << CranePos[0] << "\t, yp:" << CranePos[1] << "\t, zp:" << CranePos[2];
    cout << "\t | Delay1: " << Delay1 << "\t Delay2: " << Delay2;
    cout << "\t | Endswitch x: " << digitalRead(EndSwx) << "\t y: " << digitalRead(EndSwy)<< "\t yz " << digitalRead(EndSwz);
    cout << "\t" << endl;
}

void WriteToFile(int const (&JoystPos)[3], int const (&CranePos)[3]){  
    std::ofstream ofs;
    ofs.open("../htdocs/CranePos.txt", std::ofstream::out | std::ofstream::trunc);
    ofs << JoystPos[0] << ',' << JoystPos[1] << ',' << JoystPos[2] << ';' << CranePos[0] << ',' << CranePos[1] << ',' << CranePos[2];
    ofs.close();
}