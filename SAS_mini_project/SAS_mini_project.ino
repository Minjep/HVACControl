#include "ICMSensor.h"
#include "GNSSSensor.h"
#include <Wire.h>

constexpr struct {
  struct {
    const uint8_t trigPin = A4;
    const uint8_t echoPin = A5;
  } Pin;
  const uint32_t SerialBaudRate = 115200;
  const float samplingTime = 0;
} Global;

ICMSensor ICMSensor;
GNSSSensor GNSSSensor;



void setup() {
  // Set up a serial connection with the computer.
  Serial.begin(Global.SerialBaudRate);

  while (!Serial)
    ;



  Wire.begin();
  Wire.setClock(400000);
  delay(100);
  ICMSensor.Initialize();
  delay(100);
  GNSSSensor.Initialize();
  delay(100);
  
  
}




long lastTime = 0;
void loop() {
  if (millis() - lastTime > 3000) {
    lastTime = millis();

    //ICMSensor.UpdateMeasurements();
    /*ICMSensor.printAccValues();
    ICMSensor.printGyroValues();
    ICMSensor.printMagnoValues();
    Serial.println();*/
    //Serial.print("heading: ");
    //float heading = ICMSensor.getHeading();
    //Serial.println(heading);

    Serial.println();
    delay(100);
    GNSSSensor.UpdateValues();
    GNSSSensor.printGNSSValues();
  }
}
