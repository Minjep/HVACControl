#include <Arduino.h>
#include <BasicLinearAlgebra.h>
#include <Kalman.h>

using namespace BLA;

const int stateDim = 2;
const int inputDim = 2;
const int outputDim = 2;

Matrix<stateDim, stateDim> A = {1, 1, 0, 1};
Matrix<outputDim, stateDim> C = {1, 0, 0, 1};
Matrix<stateDim, stateDim> Q = {0.0001, 0, 0, 0.0001};
Matrix<outputDim, outputDim> R = {0.1, 0, 0, 0.1};
Matrix<outputDim, stateDim> P = {1, 0, 0, 1};
Matrix<stateDim, 1> initX = {0, 0};
Matrix<stateDim, stateDim> initP = {1, 0, 0, 1};

Kalman<stateDim, inputDim, outputDim> kf(A, C, Q, R, P);

void setup() {
  kf.init(initX, initP, 0.1);

  Matrix<stateDim, 1> z = {1, 1};
  Serial.begin(115200);
  while (1) {
    kf.predict();
    kf.update(z);

    Serial.print("X_hat = ");
    Serial << kf.getStates() << "\n";
    delay(1000);
  }
}

void loop() {
  // Empty loop function since the main code is in setup()
}