#ifndef MAGNETOMETER_H_
#define MAGNETOMETER_H_
#include <tuple>
#include <SparkFun_MMC5983MA_Arduino_Library.h>

class Magnetometer {
public:
  Magnetometer();
  SFE_MMC5983MA myMag;
  void UpdateMagnetometerMeasurements();
  std::tuple<float, float, float> GetMagnetometerMeasurements();
  void printMagnetometorValues();
  void Initialize();
  

private:
  uint32_t rawMagnoX = 0;
  uint32_t rawMagnoY = 0;
  uint32_t rawMagnoZ = 0;
  double MagnoX = 0;
  double MagnoY = 0;
  double MagnoZ = 0;
  double magScale = 131072.0;
  const int MagnetometerI2C = 0x30;
  
  
};

#endif
