#include "_DOOR.h"
#include "Arduino.h"
#include "common.h"
#include "_LCD.h"
#include "gateway.h"
#include "timer.h"

int statusOfDoor;

// Initiaization of module
void init_DOOR(){
  statusOfDoor = 0;
  pinMode(DOOR_PIN, OUTPUT);
}

// Toggle state of LED
//void toggleDOOR(){
//  statusOfDoor = 1 - statusOfDoor;
//  digitalWrite(DOOR_PIN, !digitalRead(DOOR_PIN));
//  Serial.println(task_gateway_state_DOOR(statusOfDoor));
//}

// Function to open the DOOR when scanning RFID or called by admin
void openDOOR() {
  setTimer(7, 30000); // Set timeout for DOOR
  digitalWrite(DOOR_PIN, 1);
  statusOfDoor = 1;
}

// Function to closing the DOOR when timeout
void closeDOOR() {
  if (getTimerFlag(7) == 1) {
    digitalWrite(DOOR_PIN, 0);
    statusOfDoor = 0;
  } 
}
