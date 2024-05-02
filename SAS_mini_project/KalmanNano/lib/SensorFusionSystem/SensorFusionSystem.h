#ifndef SENSORFUSIONSYSTEM_H
#define SENSORFUSIONSYSTEM_H
#include <Kalman.h>
#include <GlobalSettings.h>
#include <GNSSSensor.h>
#include <ICMSensor.h>
#include <BasicLinearAlgebra.h>
class SensorFusionSystem {
  public:
    SensorFusionSystem();
    void predict();
    void update();
    void init();
    void printStates();

  private:
    Kalman<GlobalSettings::kalmanSettings.stateDim, GlobalSettings::kalmanSettings.inputDim, GlobalSettings::kalmanSettings.outputDim> kalmanFilter;
    // Other sensors
    GNSSSensor gnssSensor;
    ICMSensor icmSensor;
    void pullSensorData();
    float posLat;  
    float posLong;
    float heading;
    float accXB;
    float accYB;
    float gyroZ;
    BLA::Matrix<GlobalSettings::kalmanSettings.outputDim, 1> z;
};
#endif