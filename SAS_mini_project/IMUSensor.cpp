#include <Arduino.h>
#include <Arduino_LSM6DS3.h>
#include "IMUSensor.h"




IMUSensor::IMUSensor() {
}

void IMUSensor::UpdateAccelerometerMeasurements() {
  IMU.readAcceleration(AccX, AccY, AccZ);
}

void IMUSensor::UpdateGyroMeasurements() {
  IMU.readGyroscope(GyroX, GyroY, GyroZ);
}

std::tuple<float, float, float> IMUSensor::GetAccelerometerMeasurements() {
  IMU.readAcceleration(AccX, AccY, AccZ);
  return std::make_tuple(AccX, AccY, AccZ);
}

std::tuple<float, float, float> IMUSensor::GetGyroMeasurements() {
  IMU.readGyroscope(GyroX, GyroY, GyroZ);
  return std::make_tuple(GyroX, GyroY, GyroZ);
}

void IMUSensor::printAccValues(){
  Serial.println();
  Serial.print(F("acc X: "));
  Serial.print(AccX);

  Serial.print(F(" acc Y: "));
  Serial.print(AccY);

  Serial.print(F(" acc Z: "));
  Serial.print(AccZ);
}

void IMUSensor::printGyroValues(){
  Serial.println();
  Serial.print(F("gyro X: "));
  Serial.print(GyroX);

  Serial.print(F(" gyro Y: "));
  Serial.print(GyroY);

  Serial.print(F(" gyro Z: "));
  Serial.print(GyroZ);
}

void IMUSensor::Initialize(){
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1)
      ;
  }
}
