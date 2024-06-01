#include "SensorFusionSystem.h"

SensorFusionSystem::SensorFusionSystem() : 
    kalmanFilter(GlobalSettings::kalmanSettings.A, GlobalSettings::kalmanSettings.C, GlobalSettings::kalmanSettings.Q, GlobalSettings::kalmanSettings.R, GlobalSettings::kalmanSettings.P,GlobalSettings::kalmanSettings.I) 
    {
       
    }
    
void SensorFusionSystem::init() {
    // init the other sensors
       
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
    BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> initX = {posLat, posLong, 0, 0, 0, 0, 0, 0, 0.0001, 0};
    Serial.print("initX = ");
    Serial << initX << "\n";
    kalmanFilter.init(initX, GlobalSettings::kalmanSettings.initP,GlobalSettings::kalmanSettings.Ts);


}
void SensorFusionSystem::pullSensorData() {
    // pull data from the sensors
    gnssSensor.UpdateValues();
    icmSensor.UpdateMeasurements();
    posLat = gnssSensor.convertLatLonToMeters().first;
    posLong = gnssSensor.convertLatLonToMeters().second;
    heading = icmSensor.getHeading();
   
    
    heading = heading * (PI/180);
    std::tuple<float, float, float> acc= icmSensor.GetAccelerometerMeasurements();
    accXB = std::get<0>(acc);
    accYB = std::get<1>(acc);
    std::tuple<float, float, float> gyro= icmSensor.GetGyroMeasurements();
    gyroZ = std::get<2>(gyro);
    z = {posLat, posLong, accXB, accYB, heading,gyroZ};
    Serial.print("z = ");
    Serial<< z<<"\n";
    //icmSensor.printAccValues(); 
    //icmSensor.printGyroValues();
}

void SensorFusionSystem::predict() {
    kalmanFilter.extended_predict();
}

void SensorFusionSystem::update() {
    pullSensorData();
    kalmanFilter.update(z);
    kalmanFilter.printAllMatrices();
}
void SensorFusionSystem::printStates() {
    BLA::Matrix<GlobalSettings::kalmanSettings.stateDim, 1> states = kalmanFilter.getStates();
    Serial.print("PosX, PosY = ");
    Serial << states(0,0) << ", " << states(1,0) << "\n";
    Serial.print("Velocity = ");
    Serial << states(2,0) << ", " << states(3,0) << "\n";
    Serial.print("Heading = ");
    Serial << states(8,0) << "\n";
    }