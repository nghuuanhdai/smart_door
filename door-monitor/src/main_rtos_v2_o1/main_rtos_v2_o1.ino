// Van de chi con o timer????
#include "timer.h"
#include "_LCD.h"
#include "_button.h"
#include "_RFID.h"
#include "_LED.h"
#include "_DOOR.h"
#include "gateway.h"
#include "common.h"
#include <stdint.h>
#include "_DHT11.h"

// Save ID of task task_gateway_sending in scheduler
uint32_t ID_task_gateway;

void setup() {
  // Call initialization function of other modules
  init_LCD();
  init_button_reading();
  init_timer_interrupt();
  init_timer_software();
  init_LED();
  init_DOOR();
  init_RFID();
  init_gateway();
  init_DHT11();
}

void loop(){
  // Call other functions when have button event
  fsm_button_reading();
  // Al3ways checking abnormal in RFID checking
  RFID_checking();
  // Wait server requirement and call functions to do it
  gateway_command_received_parse();
  // Measure temperature timing for user have ID
  process_measure_temperature_demo();
  // Function closing DOOR always run to check timeout for DOOR
  closeDOOR();
}

// Interrupt service routine function
ISR(TIMER1_COMPA_vect){
  // Read signal from buttons
  button_reading();
  // Update time of software timer 
  timer_run();
}
