#include "_LED.h"
#include "Arduino.h"
#include "common.h"
#include "gateway.h"

// Initiaization of module
void init_LED(){
  pinMode(LED_PIN, OUTPUT);
}

// Toggle state of LED
void toggleLED(){
  digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  Serial.println(task_gateway_toggle_LED(digitalRead(LED_PIN)));
}

// Set the level of LED, prevent the duplicate message
void setLED(int level) {
  digitalWrite(LED_PIN, level);
}
