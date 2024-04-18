#ifndef GNSSSENSOR_H_
#define GNSSSENSOR_H_

#include <tuple>

class GNSSSensor {
public:
  GNSSSensor();
  void UpdateValues();
  long getLatitude();
  long getLongitude();
  long getAltitude();
  long getSIV();
  void printGNSSValues();
  void Initialize();

private:
  long latitude = 0;
  long longitude = 0;
  long altitude = 0;
  byte SIV=0;
};

#endif

