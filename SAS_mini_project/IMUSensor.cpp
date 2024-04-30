#include "IMUSensor.h"
#include <Arduino.h>
#include <MPU6050.h>
#include <Wire.h>

IMUSensor::IMUSensor() {
}

void IMUSensor::UpdateAccelerometerMeasurements() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // Start with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);  // Read 6 registers total, each axis value is stored in 2 registers
  if (Wire.available()) {
    rawAccX = (Wire.read() << 8 | Wire.read());  // X-axis value
    rawAccY = (Wire.read() << 8 | Wire.read());  // Y-axis value
    rawAccZ = (Wire.read() << 8 | Wire.read());  // Z-axis value
  }
  AccX = rawAccX / scaleacc;
  AccY = rawAccY / scaleacc;
  AccZ = rawAccZ / scaleacc;
}

void IMUSensor::UpdateGyroMeasurements() {
  Wire.beginTransmission(MPU);
  Wire.write(0x47);  //Specify address for gyroscope (0x47 (GYRO_ZOUT_H)
  Wire.endTransmission();
  Wire.requestFrom(MPU, 6);  // request a total of 6 registers
  if (Wire.available()) {
    rawGyroX = (Wire.read() << 8 | Wire.read());  // X-axis value
    rawGyroY = (Wire.read() << 8 | Wire.read());  // Y-axis value
    rawGyroZ = (Wire.read() << 8 | Wire.read());  // Z-axis value
  }
  //scale raw gyro data and convert to rad/s
  GyroX = (rawGyroX / gyroScale) * M_PI / 180;
  GyroY = (rawGyroZ / gyroScale) * M_PI / 180;
  GyroZ = (rawGyroZ / gyroScale) * M_PI / 180;
}




// Assign accelerometer data to variables
std::tuple<float, float, float> IMUSensor::GetAccelerometerMeasurements() {
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // Start with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU, 6, true);  // Read 6 registers total, each axis value is stored in 2 registers
  if (Wire.available()) {
    rawAccX = (Wire.read() << 8 | Wire.read());  // X-axis value
    rawAccY = (Wire.read() << 8 | Wire.read());  // Y-axis value
    rawAccZ = (Wire.read() << 8 | Wire.read());  // Z-axis value
  }
  AccX = rawAccX / scaleacc;
  AccY = rawAccY / scaleacc;
  AccZ = rawAccZ / scaleacc;
  return std::make_tuple(AccX, AccY, AccZ);
}

std::tuple<float, float, float> IMUSensor::GetGyroMeasurements() {
  Wire.beginTransmission(MPU);
  Wire.write(0x47);  //Specify address for gyroscope (0x47 (GYRO_ZOUT_H)
  Wire.endTransmission();
  Wire.requestFrom(MPU, 6);  // request a total of 6 registers
  if (Wire.available()) {
    rawGyroX = (Wire.read() << 8 | Wire.read());  // X-axis value
    rawGyroY = (Wire.read() << 8 | Wire.read());  // Y-axis value
    rawGyroZ = (Wire.read() << 8 | Wire.read());  // Z-axis value
  }
  //scale raw gyro data and convert to rad/s
  GyroX = (rawGyroX / gyroScale) * M_PI / 180;
  GyroY = (rawGyroZ / gyroScale) * M_PI / 180;
  GyroZ = (rawGyroZ / gyroScale) * M_PI / 180;
  return std::make_tuple(GyroX, GyroY, GyroZ);
}

void IMUSensor::printAccValues() {
  Serial.println();
  Serial.print(F("acc X: "));
  Serial.print(AccX);

  Serial.print(F(" acc Y: "));
  Serial.print(AccY);

  Serial.print(F(" acc Z: "));
  Serial.print(AccZ);
}

void IMUSensor::printGyroValues() {
  Serial.println();
  Serial.print(F("gyro X: "));
  Serial.print(GyroX);

  Serial.print(F(" gyro Y: "));
  Serial.print(GyroY);

  Serial.print(F(" gyro Z: "));
  Serial.print(GyroZ);
}

void IMUSensor::Initialize() {
  Wire.beginTransmission(MPU);  // Start communication with MPU6050 // MPU=0x68
  Wire.write(0x6B);             // Talk to the register 6B
  Wire.write(0x00);             // Make reset - place a 0 into the 6B register
  Wire.endTransmission(true);   //end the transmission

  //Acc config
  Wire.beginTransmission(MPU);  // Contact IMU for setup
  Wire.write(0x1C);             // ACCEL_CONFIG register
  Wire.write(0b00000000);       // Setting the accel to +/- 2g
  Wire.endTransmission();

  Wire.beginTransmission(MPU);        // Contact IMU for setup
  Wire.write(0x1B);                       // GYRO_CONFIG register
  Wire.write(0b00001000);                 // Register bits set to b'00010000 (500dps full scale)
  Wire.endTransmission();   
}
