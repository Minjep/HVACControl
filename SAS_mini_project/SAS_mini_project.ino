#include "IMUSensor.h"
#include "GNSSSensor.h"
#include "Magnetometer.h"
#include <Wire.h>

constexpr struct {
  struct {
    const uint8_t trigPin = A4;
    const uint8_t echoPin = A5;
  } Pin;
  const uint32_t SerialBaudRate = 115200;
  const float samplingTime = 0;
} Global;

IMUSensor IMUSensor;
Magnetometer Magnetometer;
GNSSSensor GNSSSensor;



void setup() {
  // Set up a serial connection with the computer.
  Serial.begin(Global.SerialBaudRate);

  while (!Serial)
    ;


  digitalWrite(2, HIGH); // sets the digital pin 13 on
  delay(1000);            // waits for a second
  digitalWrite(2, LOW);  // sets the digital pin 13 off
  delay(1000); 

  Wire.begin();
  delay(100);
  IMUSensor.Initialize();
  delay(100);
  Magnetometer.Initialize();
  delay(100);
  GNSSSensor.Initialize();
  delay(100);
}



float accelerationX, accelerationY, accelerationZ = 0;
float angularVelocityX, angularVelocityY, angularVelocityZ = 0;

long lastTime = 0;
int i = 1;
void loop() {


  if (millis() - lastTime > 1000) {
    lastTime = millis();
    Serial.println();
    //auto [accelerationX,accelerationY,accelerationZ] = IMUSensor.GetAccelerometerMeasurements();
    //auto [angularVelocityX,angularVelocityY,angularVelocityZ] = IMUSensor.GetGyroMeasurements();
    //IMUSensor.UpdateAccelerometerMeasurements();
    //Serial.println(M_PI);
    //IMUSensor.UpdateGyroMeasurements();
    //IMUSensor.printAccValues();
    //IMUSensor.printGyroValues();
    //Serial.print(i);
    //Serial.print(",");
    //i++;


    Serial.println();
    delay(100);

    Magnetometer.UpdateMagnetometerMeasurements();
    Magnetometer.printMagnetometorValues();

    Serial.println();
    delay(100);

    GNSSSensor.UpdateValues();
    GNSSSensor.printGNSSValues();
  }
}
