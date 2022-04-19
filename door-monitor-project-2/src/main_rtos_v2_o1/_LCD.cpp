#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include "_LCD.h"
#include "Arduino.h"

LiquidCrystal_I2C lcd1(0x27, 16, 2);

// Use for display degree symbol
byte degree[8] =
{
  0B01110,
  0B01010,
  0B01110,
  0B00000,
  0B00000,
  0B00000,
  0B00000,
  0B00000
};

// Extern from FAN module
extern int mode;

// Extern from DOOR module
extern int statusOfDoor;

// Extern from DHT11 module
extern float temperature;

// Extern from RFID module
extern String id;
extern int NoOfIDsoutSession;

// Initiaization of module
void init_LCD(){
  lcd1.begin();
  lcd1.backlight();
  lcd1.createChar(1, degree);
}

// LCD 1 display information about scanning RFID
void task_scanRFID_display(int mode){
  if (id.length() == 0 && mode == 0) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("RFID please!");
    if (NoOfIDsoutSession > 0) {
      lcd1.setCursor(0,1);
      lcd1.print(String(NoOfIDsoutSession) + " IDs timeout!");
    }
  }
  else if (mode == 0) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("ID: " + id);
    lcd1.setCursor(0,1);
    lcd1.print("Measure temp!");
  } 
  else if (mode == 1) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("ID: " + id);
    lcd1.setCursor(0,1);
    lcd1.print("Temp: " + String(temperature, 1));
  } 
  else if (mode == 2) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("Scan successfully!");
    lcd1.setCursor(0,1);
    lcd1.print("User out of room!"); 
  }
  else if (mode == 3) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("UserID not valid!");
  }
  else if (mode == 4) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("UserID not allow");
    lcd1.setCursor(0,1);
    lcd1.print("in room!");
  }
  else if (mode == 5) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("Out scheduling!");
    lcd1.setCursor(0,1);
    lcd1.print(String(NoOfIDsoutSession) + " people left!");
  }
  else if (mode == 6) {
    lcd1.clear();
    lcd1.setCursor(0,0);
    lcd1.print("ID out schedule!");
    lcd1.setCursor(0,1);
    lcd1.print(String(NoOfIDsoutSession) + " people left!");
  }
}
