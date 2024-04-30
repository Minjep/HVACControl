#ifndef IMUSENSOR_H_
#define IMUSENSOR_H_

#include <tuple>


class IMUSensor {
public:
  IMUSensor();
  void UpdateGyroMeasurements();
  void UpdateAccelerometerMeasurements();
  std::tuple<float, float, float> GetAccelerometerMeasurements();
  std::tuple<float, float, float> GetGyroMeasurements();
  void printAccValues();
  void printGyroValues();
  void Initialize();

private:
  float AccX{ 0.f };
  float AccY{ 0.f };
  float AccZ{ 0.f };
  int16_t rawAccX{ 0 };
  int16_t rawAccY{ 0 };
  int16_t rawAccZ{ 0 };
  float GyroX{ 0.f };
  float GyroY{ 0.f };
  float GyroZ{ 0.f };
  int16_t rawGyroX{ 0 };
  int16_t rawGyroY{ 0 };
  int16_t rawGyroZ{ 0 };
  const int MPU = 0x68;
  const float scaleacc = 16384.0;
  const float gyroScale = 65.5;  //Scale for gyroscope (From datasheet)
};

#endif