#include "ICMSensor.h"
#include <Arduino.h>
#include <Wire.h>
#include "ICM_20948.h"

ICMSensor::ICMSensor() {
}

void ICMSensor::UpdateMeasurements() {
  if (myICM.dataReady()) {
    myICM.getAGMT();  // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    AccX = myICM.accX();  //[mg]
    AccY = myICM.accY();  //[mg]
    AccZ = myICM.accZ();  // [mg]
    AccX = AccX / mg_to_m_per_s_sqaured;
    AccY = AccY / mg_to_m_per_s_sqaured;
    AccZ = AccZ / mg_to_m_per_s_sqaured;
    GyroX = myICM.gyrX();        //[degrees/s]
    GyroY = myICM.gyrY();        //[degrees/s]
    GyroZ = myICM.gyrZ();        //[degrees/s]
    GyroX = GyroX * M_PI / 180;  //[rad/s]
    GyroY = GyroY * M_PI / 180;  //[rad/s]
    GyroZ = GyroZ * M_PI / 180;  //[rad/s]
    MagnoX = myICM.magX();       //[uT]
    MagnoY = myICM.magY();       //[uT]
    MagnoZ = myICM.magZ();       //[uT]
    MagnoX = MagnoX - MagnoOffsetX;
    MagnoY = MagnoY - MagnoOffsetY;
    MagnoZ = MagnoZ - MagnoOffsetZ;
    delay(30);
  } else {
    Serial.println("Waiting for data");
    delay(500);
  }
}

float ICMSensor::getHeading() {
  // Calculate total magnetic field strength (magnitude)
  float magnitude = sqrt(MagnoX * MagnoX + MagnoY * MagnoY);

  // Normalize magnetic field measurements
  normMagnoX = MagnoX / magnitude;
  normMagnoY = MagnoY / magnitude;

  // Calculate heading angle (in degrees)
  float heading = atan2(normMagnoY, normMagnoX) * 180.0 / M_PI;

  // Adjust for declination angle
  heading += decalination_angle;

  // Ensure heading angle is within [0, 360) range
  if (heading < 0) {
    heading += 360.0;
  } else if (heading >= 360.0) {
    heading -= 360.0;
  }
  return heading;
}

// Assign accelerometer data to variables

std::tuple<float, float, float> ICMSensor::GetAccelerometerMeasurements() {
  return std::make_tuple(AccX, AccY, AccZ);
}


std::tuple<float, float, float> ICMSensor::GetGyroMeasurements() {
  return std::make_tuple(GyroX, GyroY, GyroZ);
}

std::tuple<float, float, float> ICMSensor::GetMagnoMeasurements() {
  return std::make_tuple(MagnoX, MagnoY, MagnoZ);
}

void ICMSensor::printAccValues() {
  Serial.println();
  Serial.print(F("acc X: "));
  Serial.print(AccX);

  Serial.print(F(" acc Y: "));
  Serial.print(AccY);

  Serial.print(F(" acc Z: "));
  Serial.print(AccZ);
}

void ICMSensor::printGyroValues() {
  Serial.println();
  Serial.print(F("gyro X: "));
  Serial.print(GyroX);

  Serial.print(F(" gyro Y: "));
  Serial.print(GyroY);

  Serial.print(F(" gyro Z: "));
  Serial.print(GyroZ);
}

void ICMSensor::printMagnoValues() {
  Serial.println();
  Serial.print(F("Magno X: "));
  Serial.print(MagnoX);

  Serial.print(F("Magno Y: "));
  Serial.print(MagnoY);

  Serial.print(F("Magno Z: "));
  Serial.print(MagnoZ);
}

void ICMSensor::Initialize() {
  myICM.begin(Wire, 1);
  Serial.print(F("Initialization of the sensor returned: "));
  Serial.println(myICM.statusString());
  if (myICM.status != ICM_20948_Stat_Ok) {
    Serial.println("Trying again...");
    delay(500);
  }
}
