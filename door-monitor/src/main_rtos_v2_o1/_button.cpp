#include "Arduino.h"
#include "_button.h"
#include "common.h"
#include "_RFID.h"
#include "_LED.h"
#include "_DOOR.h"

#define PRESSED LOW
#define RELEASED HIGH

#define NUMBER_OF_BUTTONS 2

enum STATE{
  BEING_RELEASED,
  BE_PRESSED,
  BEING_PRESSED
};

// Array save PIN value of buttons
int buttonPin[NUMBER_OF_BUTTONS] = {BUTTON_1_PIN, BUTTON_2_PIN};

// Array save first debounce of buttons
int buttonDebounce1[NUMBER_OF_BUTTONS];
// Array save second debounce of buttons
int buttonDebounce2[NUMBER_OF_BUTTONS];
// Array save third debounce of buttons
int buttonDebounce3[NUMBER_OF_BUTTONS];
// Array save counter of buttons
int buttonCounter[NUMBER_OF_BUTTONS];
// Array save flag of buttons
STATE buttonFlag[NUMBER_OF_BUTTONS];

// Initiaization of module
void init_button_reading(){
  pinMode(BUTTON_1_PIN, INPUT_PULLUP);
  pinMode(BUTTON_2_PIN, INPUT_PULLUP);
  for (int i = 0; i < NUMBER_OF_BUTTONS; i++){
    buttonDebounce1[i] = RELEASED;
    buttonDebounce2[i] = RELEASED;
    buttonDebounce3[i] = RELEASED;
    buttonCounter[i] = 0;
    buttonFlag[i] = BEING_RELEASED;
  }
}

// Function get signal from button
void button_reading(){
  for (int i = 0; i < NUMBER_OF_BUTTONS; i++){
    buttonDebounce1[i] = buttonDebounce2[i];
    buttonDebounce2[i] = buttonDebounce3[i];
    buttonDebounce3[i] = digitalRead(buttonPin[i]);
    if(buttonDebounce1[i] == buttonDebounce2[i] && buttonDebounce2[i] == buttonDebounce3[i]){
      if(buttonDebounce1[i] == PRESSED){
        buttonCounter[i]++;
        if(buttonCounter[i] == 1) 
          buttonFlag[i] = BE_PRESSED;
        else 
          buttonFlag[i] = BEING_PRESSED;
        // For button 1, 2, 3, 4
        buttonCounter[i] = 2;
      }
      else{
        buttonCounter[i] = 0;
        buttonFlag[i] = BEING_RELEASED;
      }
    }
  }
}

// function call other functions when have button event
void fsm_button_reading(){
  for (int i = 0; i < NUMBER_OF_BUTTONS; i++){
    switch(buttonFlag[i]){
      case BEING_RELEASED:
        break;
      case BEING_PRESSED:
        break;
      case BE_PRESSED:
        if (i == 0) openDOOR(); // For DOOR in room
        if (i == 1) toggleLED(); // For LED in room
        buttonFlag[i] = BEING_PRESSED;
        break;
      default:
        break;
    }
  }
}
