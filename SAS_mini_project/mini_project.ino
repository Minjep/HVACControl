#include "IMUSensor.h"
#include "GNSSSensor.h"
constexpr struct {
  struct {
    const uint8_t trigPin = A4;
    const uint8_t echoPin = A5;
  } Pin;
  const uint32_t SerialBaudRate = 115200;
  const float samplingTime = 0;
} Global;

IMUSensor IMUSensor;
GNSSSensor GNSSSensor;

void setup() {
  // Set up a serial connection with the computer.
  Serial.begin(Global.SerialBaudRate);
  while (!Serial)
    ;

  IMUSensor.Initialize();

  GNSSSensor.Initialize();
  delay(10000);
}



float accelerationX, accelerationY, accelerationZ = 0;
float angularVelocityX, angularVelocityY, angularVelocityZ = 0;

long lastTime = 0;
int i = 1;
void loop() {
  

  if (millis() - lastTime > 1000) {
    lastTime = millis();
    //auto [accelerationX,accelerationY,accelerationZ] = IMUSensor.GetAccelerometerMeasurements();
    //auto [angularVelocityX,angularVelocityY,angularVelocityZ] = IMUSensor.GetGyroMeasurements();
    //IMUSensor.UpdateAccelerometerMeasurements();
    //IMUSensor.UpdateGyroMeasurements();
    //IMUSensor.printAccValues();
    //IMUSensor.printGyroValues();
    Serial.print(i);
    Serial.print(",");
    i++;
    GNSSSensor.UpdateValues();
    GNSSSensor.printGNSSValues();
  }
}
