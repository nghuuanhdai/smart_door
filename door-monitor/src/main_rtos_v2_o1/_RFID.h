#ifndef __RFID.H
#define __RFID.H

#include "Arduino.h"

void init_RFID();
void RFID_checking();
void processRFID(String IDUser);
void exitSchedule();
void setupSchedule(String msgs[], int numberOfPeopleInRoom);
void process_measure_temperature_demo();

#endif
