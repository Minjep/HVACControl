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
    delay(30);
  } else {
    Serial.println("Waiting for data");
    delay(500);
  }
}

float ICMSensor::getHeading() {
  heading = atan2(AccX, 0 - AccY);

  // atan2 returns a value between +PI and -PI
  // Convert to degrees
  heading /= PI;
  heading *= 180;
  heading += 180;
  return heading;
}

// Assign accelerometer data to variables

std::tuple<float, float, float> ICMSensor::GetAccelerometerMeasurements() {
  if (myICM.dataReady()) {
    myICM.getAGMT();  // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    AccX = myICM.accX();  //[mg]
    AccY = myICM.accY();  //[mg]
    AccZ = myICM.accZ();  // [mg]
    AccX = AccX / mg_to_m_per_s_sqaured;
    AccX = AccX / mg_to_m_per_s_sqaured;
    AccX = AccX / mg_to_m_per_s_sqaured;
    delay(30);
  } else {
    Serial.println("Waiting for data");
    delay(500);
  }
  return std::make_tuple(AccX, AccY, AccZ);
}


std::tuple<float, float, float> ICMSensor::GetGyroMeasurements() {
  if (myICM.dataReady()) {
    myICM.getAGMT();  // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    GyroX = myICM.gyrX();        //[degrees/s]
    GyroY = myICM.gyrY();        //[degrees/s]
    GyroZ = myICM.gyrZ();        //[degrees/s]
    GyroX = GyroX * M_PI / 180;  //[rad/s]
    GyroY = GyroY * M_PI / 180;  //[rad/s]
    GyroZ = GyroZ * M_PI / 180;  //[rad/s]
    delay(30);
  } else {
    Serial.println("Waiting for data");
    delay(500);
  }
  return std::make_tuple(GyroX, GyroY, GyroZ);
}

std::tuple<float, float, float> ICMSensor::GetMagnoMeasurements() {
  if (myICM.dataReady()) {
    myICM.getAGMT();  // The values are only updated when you call 'getAGMT'
    //    printRawAGMT( myICM.agmt );     // Uncomment this to see the raw values, taken directly from the agmt structure
    MagnoX = myICM.magX();  //[uT]
    MagnoY = myICM.magY();  //[uT]
    MagnoZ = myICM.magZ();  //[uT]
    delay(30);
  } else {
    Serial.println("Waiting for data");
    delay(500);
  }
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
