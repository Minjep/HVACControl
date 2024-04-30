#pragma once

#include <Arduino.h>
#include <BasicLinearAlgebra.h>

using namespace BLA;

template <int stateDim, int inputDim, int outputDim,float>
class Kalman {
public:
    Kalman(const Matrix<stateDim, stateDim,float>& A, const Matrix<outputDim, stateDim,float>& C,
           const Matrix<stateDim, stateDim,float>& Q, const Matrix<outputDim, outputDim,float>& R,
           const Matrix<outputDim, stateDim,float>& P);

    void init(const Matrix<stateDim, 1>& initX, const Matrix<stateDim, stateDim,float>& initP, double dt);
    void predict();
    void specialBpredict(const Matrix<stateDim, inputDim,float>& B, const Matrix<inputDim, 1>& u);
    void update(const Matrix<outputDim, 1>& z);
    Matrix<stateDim, 1> getStates() const;

private:
    Matrix<stateDim, stateDim,float> A_;
    Matrix<outputDim, stateDim,float> C_;
    Matrix<stateDim, stateDim,float> Q_;
    Matrix<outputDim, outputDim,float> R_;
    Matrix<outputDim, stateDim,float> P_;
    Matrix<stateDim, stateDim,float> Pp_;
    Matrix<stateDim, 1> X_hat_;
    Matrix<stateDim, 1> X_pred_;
    Matrix<stateDim, stateDim,float> K_;
    Matrix<outputDim, outputDim,float> I_;
    double dt_;
};