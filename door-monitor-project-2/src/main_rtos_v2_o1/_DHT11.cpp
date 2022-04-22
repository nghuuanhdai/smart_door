#include <DHT.h>
#include "common.h"
#include "_DHT11.h"
#include "Arduino.h"

const int DHTTYPE = DHT11;
DHT dht(DHTPIN, DHTTYPE);

// Save temperature value is read from DHT11 sensor
float temperature; 
// Save humidity value is read from DHT11 sensor
float humidity;


// Initiaization of module
void init_DHT11(){
  dht.begin();
}

void task_measure_human_temperature(){
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  // Check if reading from DHT11 successfully 
  if(!isnan(t) && !isnan(h)){
    temperature = t;
    humidity = h;
  }
}
