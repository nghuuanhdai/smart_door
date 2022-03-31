#include "_RFID.h"
#include "Arduino.h"
#include "timer.h"
#include "common.h"
#include "_LCD.h"
#include "_DHT11.h"
#include "gateway.h"
#include "_DOOR.h"
#include <stdint.h>


#define NO_OF_CHAR_ID 7 // IDs of lab have most 7 characters

// Array save ID of cards in system, which get from DB
// Suppose default we have 2 card IDs
String IDs[MAX_OF_IDS] = {"", "", "", "", ""};

// Prev IDs in case out of schedule still have people in room
String prevIDs[MAX_OF_IDS];
// Array save the status IN/OUT room of all IDs
int statusInRoom[MAX_OF_IDS];  
// Number of current cards in system in current time
int curNoOfIDs = 0;
// Number of cards in system in previous scheduling
int curNoOfIDsPrev = 0;
// Number of cards left when timeout in previous scheduling
int NoOfIDsoutSession = 0;
// Determine person consider
int person = -1;

// Number of people in room
int numOfPersonInRoom = 0;

// Save ID read from terminal
String id = "";
// Reading temperature from DHT11
extern float temperature;
// Save character read from terminal
char rcvChar;
// If receive '$'(character before starting to input ID) character it's value will be 1, else will be 0
bool detect_receive_id = 0;

// For beautiful the LED 16x2
// The initial state need not care about out of scheduling
int firstTime = 1;

// Exit of module
void exit_RFID(){
  id = "";
  resetTimer(0);
  setTimer(0, TIMEOUT_WAITING_INPUT); // Waiting to user see the status of themselves
}

// Function end operation of schedule
void exitSchedule(){
  //Serial.println(F("\r\nExit schedule!"));
  //Serial.println(F("All activity is rejected!"));
  for (int i = 0; i < curNoOfIDs; i++) {
    if (statusInRoom[i] != 0) {
      setTimer(i + 1, 30000); // Person i + 1 have only 30s to out of room
      prevIDs[i] = IDs[i]; // Save the IDs to save the newer IDs in this position
      NoOfIDsoutSession++;
    }
    else {
      prevIDs[i] = "";
      resetTimer(i + 1);
    }
    IDs[i] = "";
  }
  curNoOfIDsPrev = curNoOfIDs;
}

//Function setup operation of schedule
void setupSchedule(String msgs[], int numberOfPeopleInRoom) {
  int threadLCD = 0; // May be occur one of 2 LCD command
  for (int i = 0; i < MAX_OF_IDS; i++) {
    statusInRoom[i] = 0; // All people not in room!
    if (i >= numberOfPeopleInRoom)
      IDs[i] = ""; // Reset person!
    else {
      IDs[i] = msgs[i];
      // If people in previous scheduling timeout-ing is still on scheduling
      // Not set up timeout for them because we allow doing in next session
      // It occur when 2 session occur which delay short!
      for (int j = 0; j < curNoOfIDsPrev; j++) {
        if (prevIDs[j] == msgs[i]) {
          prevIDs[j] = "";
          resetTimer(j + 1);
          NoOfIDsoutSession--;
          // Because they in room but they dont need to consider timeout
          // It save time for this person
          statusInRoom[i] = 1;
          Serial.println(task_gateway_sending_remove_timeout(IDs[i]));
          break;
        }
      }
    }
  }
  curNoOfIDs = numberOfPeopleInRoom;
  if (id != "") {
    threadLCD = 1;
    bool foundPeopleMeasure = 0;
    // Have measure is doing measure temperature
    // Checking the people allow in next scheduling or not
    // If yes --> Allow measure normal but this code should revalue of person
    // If no --> Remove the session measure temp and show timeout and not allow in room
    for (int i = 0; i < numberOfPeopleInRoom; i++) {
      if (id == msgs[i]) {
        person = i;
        foundPeopleMeasure = 1;
        break;
      }
    }
    if (foundPeopleMeasure == 0) {
      resetTimer(6);
      task_scanRFID_display(6);
      exit_RFID();
    }
  }
  if (firstTime == 0) {
    if (threadLCD == 0) {
      task_scanRFID_display(5);
      exit_RFID();
    }
  }
  else
    firstTime = 0;
}

// Initialization of module
void init_RFID(){
  Serial.begin(9600);
  for (int i = 0; i < MAX_OF_IDS; i++)
    statusInRoom[i] = 0; // All people not in room!
  task_scanRFID_display(0);
}

// Function reading RFID
void processRFID(String IDUser){
  id = IDUser;
  if (id.length() < NO_OF_CHAR_ID) {
     task_scanRFID_display(3);
     exit_RFID();
  }
  if (id.length() == NO_OF_CHAR_ID) {
     int i;
     for (i = 0; i < curNoOfIDs; i++) {
       if (id == IDs[i]) {
        person = i;
        if (statusInRoom[i] == 0) {
          task_scanRFID_display(0);
          setTimer(6, TIMEOUT_DEMO_TEMPERATURE);
        }
        else {
          Serial.println(task_gateway_sending_outroom(id));
          statusInRoom[i] = 0;
          numOfPersonInRoom--;
          Serial.println(task_gateway_count_people());
          openDOOR();
          task_scanRFID_display(2);
          exit_RFID();
        }
        break;
      }
     }
     if (i >= curNoOfIDs){
      for (i = 0; i < curNoOfIDsPrev; i++) {
        if (id == prevIDs[i]) {
          Serial.println(task_gateway_sending_outroom(id));
          prevIDs[i] = "";
          resetTimer(i + 1);
          numOfPersonInRoom--;
          NoOfIDsoutSession--;
          Serial.println(task_gateway_count_people());
          openDOOR();
          task_scanRFID_display(2);
          exit_RFID();
          break;
        }
      }
      if (i >= curNoOfIDsPrev) {
        task_scanRFID_display(4);
        exit_RFID();
      }
    }
  }
}

void process_measure_temperature_demo() {
  if (getTimerFlag(6) == 1 && id != "") {
    task_measure_human_temperature();
    if (temperature >= 38) {
      Serial.println(task_gateway_sending_inroom(id, temperature));
      task_scanRFID_display(1);
    }
    else {
      statusInRoom[person] = 1;
      numOfPersonInRoom++;
      Serial.println(task_gateway_sending_inroom(id, temperature));
      Serial.println(task_gateway_count_people());
      task_scanRFID_display(1);
      openDOOR();
    }
    resetTimer(6);
    exit_RFID();
  }
}

// RFID checking is always consider abnormal case
void RFID_checking(){
  if (getTimerFlag(0) == 1) {
    task_scanRFID_display(0);
    resetTimer(0);
  }
  for (int i = 0; i < curNoOfIDsPrev; i++) {
    if (prevIDs[i] != "" && getTimerFlag(i + 1) == 1) {
      Serial.println(task_gateway_message_timeout(prevIDs[i]));

      // We can not understand for case muddy people! If have it, the system should be 
      // in the garbage because no have device can stand all cases. AI be lose for this case
      prevIDs[i] = "";
      numOfPersonInRoom--;
      resetTimer(i + 1);
      NoOfIDsoutSession--;
      task_scanRFID_display(0);
      Serial.println(task_gateway_count_people());
    }
  }
}
