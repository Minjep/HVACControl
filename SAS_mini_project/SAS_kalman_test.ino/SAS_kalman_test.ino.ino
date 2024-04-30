#include <Arduino.h>
#include <BasicLinearAlgebra.h>
#include "Kalman.h"

using namespace BLA;

const int stateDim  = 8;
const int inputDim = 3;
const int outputDim = 3;
int Ts=1000;
Matrix<stateDim, stateDim> A = {1,0,Ts,0,0,0,0,0,
                                0,1,0,Ts,0,0,0,0,
                                0,0,1,0,Ts,0,0,0,
                                0,0,0,1,0,Ts,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,0,0,
                                0,0,0,0,0,0,1,0,
                                0,0,0,0,0,0,0,0};
Matrix<stateDim, inputDim> B = {0,0,0,
                                0,0,0,
                                0,0,0,
                                0,0,0,
                                1,0,0,
                                0,1,0,
                                0,0,1,
                                0,0,0}; // This B will be updated before each prediction step
Matrix<outputDim, stateDim> C = {1,0,0,0,0,0,0,0,
                                0,1,0,0,0,0,0,0,
                                0,0,0,0,0,0,1,0};
Matrix<stateDim, stateDim> Q;
Matrix<outputDim, outputDim> R ;
Matrix<outputDim, stateDim> P ;
Matrix<stateDim, 1> initX;
Matrix<stateDim, stateDim> initP;

Kalman<stateDim, inputDim, outputDim> kf(A, C, Q, R, P);

void setup() {
  kf.init(initX, initP, 0.1);

  Matrix<outputDim, 1> z = {1, 1,1};
  Matrix<inputDim, 1> u = {1, 1,1};

  Serial.begin(115200);
  while (1) {
  Matrix<stateDim, 1> X_hat = kf.getStates();
  float Theta=X_hat(6,0);

  B = {0,0,0,
      0,0,0,  
      0,0,0,
      0,0,0,
      cos(Theta),sin(Theta),0,
      -sin(Theta),cos(Theta),0,
      0,Ts,0,
      0,0,1};
    kf.specialBpredict(B, u);
    kf.update(z);

    Serial.print("X_hat = ");
    Serial << kf.getStates() << "\n";
    delay(1000);
  }
}

void loop() {
  // Empty loop function since the main code is in setup()
}