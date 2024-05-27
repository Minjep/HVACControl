#ifndef GNSSSENSOR_H_
#define GNSSSENSOR_H_


#include <SparkFun_u-blox_GNSS_v3.h>
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
  std::pair<double, double> convertLatLonToMeters();




private:
  long rawLatitude = 0;
  long rawLongitude = 0;
  double latitude = 0;
  double longitude = 0;
  long altitude = 0;
  byte SIV = 0;
  SFE_UBLOX_GNSS myGNSS;
  const int GNSSI2C = 0x42;
  const double METERS_PER_DEGREE_LAT = 111320.0;
  double latMeters{ 0.f };
  double lonMeters{ 0.f };
  const double CONVERT_RAW_GNSS_DATA = 0.0000001;
};

#endif
