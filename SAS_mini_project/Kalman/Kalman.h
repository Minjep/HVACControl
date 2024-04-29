#pragma once

#include <Arduino.h>
#include <BasicLinearAlgebra.h>

using namespace BLA;

template <int stateDim, int inputDim, int outputDim>
class Kalman {
public:
    Kalman(const Matrix<stateDim, stateDim>& A, const Matrix<outputDim, stateDim>& C,
           const Matrix<stateDim, stateDim>& Q, const Matrix<outputDim, outputDim>& R,
           const Matrix<outputDim, stateDim>& P);

    void init(const Matrix<stateDim, 1>& initX, const Matrix<stateDim, stateDim>& initP, double dt);
    void predict();
    void update(const Matrix<stateDim, 1>& z);
    Matrix<stateDim, 1> getStates() const;

private:
    Matrix<stateDim, stateDim> A_;
    Matrix<outputDim, stateDim> C_;
    Matrix<stateDim, stateDim> Q_;
    Matrix<outputDim, outputDim> R_;
    Matrix<outputDim, stateDim> P_;
    Matrix<stateDim, stateDim> Pp_;
    Matrix<stateDim, 1> X_hat_;
    Matrix<stateDim, 1> X_pred_;
    Matrix<stateDim, stateDim> K_;
    Matrix<outputDim, outputDim> I_;
    double dt_;
};