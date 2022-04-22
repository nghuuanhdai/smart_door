#include "common.h"
#include "timer.h"
#include "Arduino.h"

#define NUMBER_OF_SOFTWARE_TIMER 8
/*
  Timer 0 --> LCD showing slow!
  Timer 1, 2, 3, 4, 5 --> Timeout 5 person when out of scheduling!
  Timer 6 --> Measure temperature slow due to doing demo!
  Timer 7 --> Session of DOOR open!
*/

int timerCounter[NUMBER_OF_SOFTWARE_TIMER];
int timerFlag[NUMBER_OF_SOFTWARE_TIMER];

void setTimer(int index, int duration){
  if(index >= NUMBER_OF_SOFTWARE_TIMER) return;
  timerCounter[index] = duration / TIMER_CYCLE;
  timerFlag[index] = 0;
}

int getTimerFlag(int index){
  if(index >= NUMBER_OF_SOFTWARE_TIMER) return -1;
  return timerFlag[index];
}

void resetTimer(int index){
  if(index >= NUMBER_OF_SOFTWARE_TIMER) return;
  timerCounter[index] = 0;
  timerFlag[index] = 0;
}

void timer_run(){
  for(int i = 0; i < NUMBER_OF_SOFTWARE_TIMER; i++){
    if(timerCounter[i] > 0){
      timerCounter[i]--;
      if(timerCounter[i] == 0) timerFlag[i] = 1;
    }
  }
}

void init_timer_software(){
  for(int i = 0; i < NUMBER_OF_SOFTWARE_TIMER; i++){
    setTimer(i, TIMER_CYCLE);
  }
}

void init_timer_interrupt(){
  cli(); // stop interrupts
  TCCR1A = 0; // set entire TCCR1A register to 0
  TCCR1B = 0; // same for TCCR1B
  TCNT1  = 0; // initialize counter value to 0
  // set compare match register for 100 Hz increments
  OCR1A = 19999; // = 16000000 / (8 * 100) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12, CS11 and CS10 bits for 8 prescaler
  TCCR1B |= (0 << CS12) | (1 << CS11) | (0 << CS10);
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei(); // allow interrupts
  
}
