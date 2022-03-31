#include "Arduino.h"
#include "gateway.h"
#include "_LED.h"
#include "_DOOR.h"
#include "_RFID.h"
#include "common.h"

// Save state of RFID 
extern int stateRFID;

//Save number of person in room
extern int numOfPersonInRoom;

enum RECEIVE_STATE{
  WAITING,
  RECEIVING
};

// Save character received 
char char_rcv;
// Save command received
String command;
// Save state of gateway receiving
RECEIVE_STATE rcv_state = WAITING;

// Initiaization of module
void init_gateway(){
  //Serial1.begin(9600);
}

// Function gateway receiving
void gateway_command_received_parse(){
  // If RFID not run and have require from server
  if(Serial.available() > 0){
    char_rcv = Serial.read();
    switch(rcv_state){
      case WAITING:
        if(char_rcv == '#') {
          rcv_state = RECEIVING;
          Serial.print(char_rcv);
        }
        break;
      case RECEIVING:
        if(char_rcv != '*'){
          Serial.print(char_rcv);
          command += char_rcv;
        }
        else{
          Serial.println();
          if (command == ("ROOM " + String(ROOM_ID) + " LED_ON")){
            setLED(1);
          }
          else if (command == ("ROOM " + String(ROOM_ID) + " LED_OFF")){
            setLED(0);
          }
          else if (command == ("ROOM " + String(ROOM_ID) + " DOOR_OPEN")){
            openDOOR();
          }
          else {
            int StringCount = 0;
            /*
             * In JSON have 2 field is IDs and ROOM 
             * IDs need MAX_OF_IDS space to store them
             * ROOM need 1 space to store
             * So the max number of elements in split array is:
             * MAX_OF_IDS + 1 + 2 = MAX_OF_IDS + 3
             */
            String split[MAX_OF_IDS + 3];
            for (int i = 0; i < MAX_OF_IDS + 3; i++)
              split[i] = "";
            while (command.length() > 0)
            {
              int index = command.indexOf(' ');
              if (index == -1) { // No space found
                split[StringCount++] = command;
                break;
              }
              else {
                split[StringCount++] = command.substring(0, index);
                command = command.substring(index + 1);
              }
            }
            if (split[1] == ROOM_ID) {
              if (split[2] == "SCHEDULE_BEGIN") {
                String IDsField[MAX_OF_IDS];
                for (int i = 3; i < MAX_OF_IDS + 3; i++)
                  IDsField[i - 3] = split[i];
                exitSchedule();
                setupSchedule(IDsField, StringCount - 3);
              }
              else if (split[2] == "USERID_SCAN")
                processRFID(split[3]);
            }
          }
          command = "";
          rcv_state = WAITING;
        }
        break;
      default:
        break;
    }
  }
}

String task_gateway_sending_outroom(String IDs) {
  return "*ROOM " + String(ROOM_ID) + " ID " + IDs + " STATUS OUT_ROOM#";
}

String task_gateway_sending_inroom(String IDs, float temperature) {
  if (temperature >= 38)
    return "*ROOM " + String(ROOM_ID) + " ID " + IDs + " TEMPERATURE " + String(temperature, 1) + " STATUS NOT_ALLOW#";
  else
    return "*ROOM " + String(ROOM_ID) + " ID " + IDs + " TEMPERATURE " + String(temperature, 1) + " STATUS ALLOW#";
}

String task_gateway_toggle_LED(int level) {
  return "*ROOM " + String(ROOM_ID) + " LED " + String(level) + "#";
}

String task_gateway_count_people() {
  return "*ROOM " + String(ROOM_ID) + " NUMPEOPLE " + String(numOfPersonInRoom) + "#";
}

String task_gateway_message_timeout(String id) {
  return "*ROOM " + String(ROOM_ID) + " ID " + id + " STATUS TIMEOUT_SCHEDULING#";
}

String task_gateway_sending_remove_timeout(String id) {
  return "*ROOM " + String(ROOM_ID) + " ID " + id + " STATUS REMOVE_TIMEOUT#";
}
