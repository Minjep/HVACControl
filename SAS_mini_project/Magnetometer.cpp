#include "Magnetometer.h"
#include "wiring_private.h"
#include <Arduino.h>
#include <Wire.h>


Magnetometer::Magnetometer() {
}

void Magnetometer::UpdateMagnetometerMeasurements() {
  rawMagnoX = myMag.getMeasurementX();
  rawMagnoY = myMag.getMeasurementY();
  rawMagnoZ = myMag.getMeasurementZ();

  // The magnetic field values are 18-bit unsigned. The _approximate_ zero (mid) point is 2^17 (131072).
  // Here we scale each field to +/- 1.0 to make it easier to convert to Gauss.
  MagnoX = (double)rawMagnoX - magScale;
  MagnoX /= magScale;
  MagnoY = (double)rawMagnoY - magScale;
  MagnoY /= magScale;
  MagnoZ = (double)rawMagnoZ - magScale;
  MagnoZ /= magScale;
}


// Assign accelerometer data to variables
std::tuple<float, float, float> Magnetometer::GetMagnetometerMeasurements() {
  rawMagnoX = myMag.getMeasurementX();
  rawMagnoY = myMag.getMeasurementY();
  rawMagnoZ = myMag.getMeasurementZ();

  // The magnetic field values are 18-bit unsigned. The _approximate_ zero (mid) point is 2^17 (131072).
  // Here we scale each field to +/- 1.0 to make it easier to convert to Gauss.
  MagnoX = (double)rawMagnoX - magScale;
  MagnoX /= magScale;
  MagnoY = (double)rawMagnoY - magScale;
  MagnoY /= magScale;
  MagnoZ = (double)rawMagnoZ - magScale;
  MagnoZ /= magScale;

  return std::make_tuple(MagnoX, MagnoY, MagnoZ);
}


void Magnetometer::printMagnetometorValues() {
  Serial.print("X axis field (Gauss): ");
  Serial.print(MagnoX * 8, 5);  //*8 to get gauss

  Serial.print("\tY axis field (Gauss): ");
  Serial.print(MagnoY * 8, 5);  //*8 to get gauss

  Serial.print("\tZ axis field (Gauss): ");
  Serial.println(MagnoZ * 8, 5);  //*8 to get gauss
}

void Magnetometer::Initialize() {
  Serial.println("123456789");
  TwoWire myWire(&sercom3, 6, 5);  // Create the new wire instance assigning it to pin 6 and 5
  //myWire.begin(MagnetometerI2C);                // join i2c bus with address #2
  pinPeripheral(6, PIO_SERCOM_ALT);  //Assign SDA function to pin 6
  pinPeripheral(5, PIO_SERCOM_ALT);
  Serial.println("098765");
  if (myMag.begin(myWire) == false) {
    digitalWrite(2, HIGH);  // sets the digital pin 13 on
    delay(1000);             // waits for a second
    digitalWrite(2, LOW);   // sets the digital pin 13 off
    delay(1000);             // waits for a second
    Serial.println("MMC5983MA did not respond - check your wiring. Freezing.");
    //while (true)
    //  ;
  }
  digitalWrite(2, HIGH); // sets the digital pin 13 on
  delay(1000);            // waits for a second
  digitalWrite(2, LOW);  // sets the digital pin 13 off
  delay(1000);            // waits for a second
  Serial.println("pefekt");
  myMag.softReset();
}
