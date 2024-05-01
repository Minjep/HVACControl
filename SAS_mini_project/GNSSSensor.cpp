#include <Arduino.h>
#include "GNSSSensor.h"





GNSSSensor::GNSSSensor() {
}

void GNSSSensor::UpdateValues() {
  rawLatitude = myGNSS.getLatitude();
  rawLongitude = myGNSS.getLongitude();
  latitude = rawLatitude * CONVERT_RAW_GNSS_DATA;
  longitude = rawLongitude * CONVERT_RAW_GNSS_DATA;
  altitude = myGNSS.getAltitude();
  SIV = myGNSS.getSIV();
}

long GNSSSensor::getLatitude() {
  return latitude;
}

long GNSSSensor::getLongitude() {
  return longitude;
}
long GNSSSensor::getAltitude() {
  return altitude;
}

long GNSSSensor::getSIV() {
  return SIV;
}


void GNSSSensor::printGNSSValues() {
  //Serial.print(F("Lat,"));
  Serial.print(latitude);

  Serial.print(F(","));
  Serial.print(longitude);
  //Serial.print(F(" (degrees * 10^-7)"));

  Serial.print(F(","));
  Serial.print(altitude);
  //Serial.print(F(" (mm)"));
  Serial.println();
}

void GNSSSensor::Initialize() {
  if (myGNSS.begin() == false)  //Connect to the u-blox module using Wire port
  {
    Serial.println(F("u-blox GNSS not detected at default I2C address. Please check wiring. Freezing."));
    while (1)
      ;
  }

  myGNSS.setI2COutput(COM_TYPE_UBX);                  //Set the I2C port to output UBX only (turn off NMEA noise)
  myGNSS.saveConfigSelective(VAL_CFG_SUBSEC_IOPORT);  //Save (only) the communications port settings to flash and BBR
  myGNSS.setNavigationFrequency(1);
}

std::pair<double, double> GNSSSensor::convertLatLonToMeters() {
  // Latitude conversion: straightforward multiplication
  latMeters = latitude * METERS_PER_DEGREE_LAT;

  // Longitude conversion: depends on latitude
  lonMeters = longitude * METERS_PER_DEGREE_LAT * cos(latitude * DEG_TO_RAD);

  return { latMeters, lonMeters };
}