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
  float GyroX{ 0.f };
  float GyroY{ 0.f };
  float GyroZ{ 0.f };
};

#endif