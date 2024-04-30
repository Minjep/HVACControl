#ifndef IMUSENSOR_H_
#define IMUSENSOR_H_

#include <tuple>
#include "ICM_20948.h"


class ICMSensor {
public:
  ICMSensor();
  void UpdateMeasurements();
  std::tuple<float, float, float> GetAccelerometerMeasurements();
  std::tuple<float, float, float> GetGyroMeasurements();
  std::tuple<float, float, float> GetMagnoMeasurements();
  void printAccValues();
  void printGyroValues();
  void printMagnoValues();
  void Initialize();
  float getHeading();

private:
  ICM_20948_I2C myICM;
  const float mg_to_m_per_s_sqaured = 101.833;  //1000/9.82
  float AccX{ 0.f };
  float AccY{ 0.f };
  float AccZ{ 0.f };
  float GyroX{ 0.f };
  float GyroY{ 0.f };
  float GyroZ{ 0.f };
  float MagnoX{ 0.f };
  float MagnoY{ 0.f };
  float MagnoZ{ 0.f };
  float heading{ 0.f };
};

#endif