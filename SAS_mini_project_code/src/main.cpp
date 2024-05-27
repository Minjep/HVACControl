#include <Arduino.h>
#include <BasicLinearAlgebra.h>
#include <Kalman.h>
#include <GlobalSettings.h>
#include <GNSSSensor.h>
#include <ICMSensor.h>
#include <Nextion.h>
NexNumber NumberPos1 =  NexNumber(1, 3, "pos1");
NexNumber NumberPos2 =  NexNumber(1, 4, "pos2");
NexNumber NumberSpeed1 =  NexNumber(2, 6, "speed1");
NexNumber NumberSpeed2 =  NexNumber(2, 7, "speed2");
NexGauge NumberCompass =  NexGauge(3, 3, "z0");
GNSSSensor gnssSensor;
ICMSensor icmSensor;
Kalman<GlobalSettings::kalmanSettings.stateDim,GlobalSettings::kalmanSettings.inputDim,GlobalSettings::kalmanSettings.outputDim> kalmanFilter(GlobalSettings::kalmanSettings.A, GlobalSettings::kalmanSettings.C, GlobalSettings::kalmanSettings.Q, GlobalSettings::kalmanSettings.R, GlobalSettings::kalmanSettings.P,GlobalSettings::kalmanSettings.I);
float posLat,posLong,heading,accXB,accYB,gyroZ;
BLA::Matrix<GlobalSettings::kalmanSettings.outputDim, 1> z;
unsigned long lastmillis;
void printCorrect(BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> states, BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> predicted,BLA::Matrix<GlobalSettings::kalmanSettings.outputDim, 1> z);
void setup() {
    Serial.begin(115200);
    delay(4000);
    Serial.println("Starting...");
   Wire.begin();
    Wire.setClock(400000);
    delay(100);
    icmSensor.Initialize();
    delay(100);
    gnssSensor.Initialize();
    delay(100);
    gnssSensor.UpdateValues();
    posLat = gnssSensor.convertLatLonToMeters().first;
    posLong = gnssSensor.convertLatLonToMeters().second;
    BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> initX = {posLong,posLat, 0, 0, 0, 0, 0, 0, 0.0001, 0};
    Serial.print("initX = ");
    Serial << initX << "\n";
    kalmanFilter.initMatrices(GlobalSettings::kalmanSettings.A, GlobalSettings::kalmanSettings.C, GlobalSettings::kalmanSettings.Q, GlobalSettings::kalmanSettings.R, GlobalSettings::kalmanSettings.P,GlobalSettings::kalmanSettings.I);
    kalmanFilter.init(initX, GlobalSettings::kalmanSettings.initP,GlobalSettings::kalmanSettings.Ts);
    bool DisplayReady = nexInit();

    delay(200);

    // put your setup code here, to run once:
    if (!DisplayReady)
    {
      Serial.println("Display not ready!");
      while(true);
    }
}

void loop() {
  if ((millis() -lastmillis) > 500){
  //Serial.println(millis() -lastmillis);
   
  kalmanFilter.extended_predict();
  gnssSensor.UpdateValues();
  icmSensor.UpdateMeasurements();
  posLat = gnssSensor.convertLatLonToMeters().first;
  posLong = gnssSensor.convertLatLonToMeters().second;
  heading = icmSensor.getHeading();
  heading =heading - 90;
  if (heading <0)
  {
    heading = heading + 360;
  }
  
  heading = heading * (PI/180);
  

  std::tuple<float, float, float> acc= icmSensor.GetAccelerometerMeasurements();
  accXB = std::get<0>(acc);
  accYB = std::get<1>(acc);
  std::tuple<float, float, float> gyro= icmSensor.GetGyroMeasurements();
  gyroZ = std::get<2>(gyro);
  z = {posLong,posLat, -accXB, accYB, heading,gyroZ};
  
  kalmanFilter.update(z);
  lastmillis = millis();
  BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> states = kalmanFilter.getStates();
  printCorrect(states,kalmanFilter.getPredicted(),z); 
  NumberPos1.setValue(states(0,0));
  NumberPos2.setValue(states(1,0));
  NumberSpeed1.setValue(states(2,0));
  NumberSpeed2.setValue(states(3,0));
  float heading = states(8,0) * (180/PI);
  // shift the heading such that N is 90 degrees

  heading = 90 - heading;
  if (heading < 0)
  {
    heading = heading + 360;
  }
  NumberCompass.setValue(heading);
  
  //kalmanFilter.printAllMatrices();
  }
  delay(2);

}

void printCorrect(BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> states, BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> predicted,BLA::Matrix<GlobalSettings::kalmanSettings.outputDim, 1> z)
{
  Serial << states(0,0) << ", " << states(1,0) << ", " << states(2,0) << ", " << states(3,0) << ", " <<  states(4,0) << ", " << states(5,0) << ", " <<  states(6,0) << ", " << states(7,0) << ", " <<  states(8,0) << ", " << states(9,0) << "\n";
  Serial << predicted(0,0) << ", " << predicted(1,0) << ", " <<  predicted(2,0) << ", " << predicted(3,0) << ", " <<  predicted(4,0) << ", " << predicted(5,0) << ", " <<  predicted(6,0) << ", " << predicted(7,0) << ", " <<  predicted(8,0) << ", " << predicted(9,0) << "\n";
  Serial << z(0,0) << ", " << z(1,0) << ", " <<  z(2,0) << ", " << z(3,0) << ", " <<  z(4,0) << ", " << z(5,0) << "\n";
} 