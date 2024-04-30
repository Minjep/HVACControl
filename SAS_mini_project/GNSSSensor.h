#ifndef GNSSSENSOR_H_
#define GNSSSENSOR_H_


#include <SparkFun_u-blox_GNSS_v3.h> 



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
  SFE_UBLOX_GNSS myGNSS;
  const int GNSSI2C = 0x42;
};

#endif

