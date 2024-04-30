#include"Kalman.h"

template <int stateDim, int inputDim, int outputDim,float>
Kalman<stateDim, inputDim, outputDim,float>::Kalman(const Matrix<stateDim, stateDim,float>& A,
                                              const Matrix<outputDim, stateDim,float>& C,
                                              const Matrix<stateDim, stateDim,float>& Q,
                                              const Matrix<outputDim, outputDim,float>& R,
                                              const Matrix<outputDim, stateDim,float>& P)
    : A_(A), C_(C), Q_(Q), R_(R), P_(P), I_(Matrix<outputDim, outputDim,float>::Identity()) {}

template <int stateDim, int inputDim, int outputDim,float>
void Kalman<stateDim, inputDim, outputDim,float>::init(const Matrix<stateDim, 1>& initX,
                                                 const Matrix<stateDim, stateDim,float>& initP, double dt) {
    X_hat_ = initX;
    P_ = initP;
    dt_ = dt;
}

template <int stateDim, int inputDim, int outputDim,float>
void Kalman<stateDim, inputDim, outputDim,float>::predict() {
    X_pred_ = A_ * X_hat_;
    Pp_ = A_ * P_ * ~A_ + Q_;
}
template <int stateDim, int inputDim, int outputDim,float>
void Kalman<stateDim, inputDim, outputDim,float>::specialBpredict(const Matrix<stateDim, inputDim,float>& B, const Matrix<inputDim, 1>& u) {
    X_pred_ = A_ * X_hat_ + B * u;
    Pp_ = A_ * P_ * ~A_ + Q_;
}


template <int stateDim, int inputDim, int outputDim,float>
void Kalman<stateDim, inputDim, outputDim,float>::update(const Matrix<outputDim, 1>& z) {
    K_ = P_ * ~C_ * (C_ * P_ * ~C_ + R_).Inverse();
    X_hat_ = X_pred_ + K_ * (z - C_ * X_pred_);
    P_ = (I_ - K_ * C_) * Pp_ * ~(I_ - K_ * C_) + K_ * R_ * ~K_;
}

template <int stateDim, int inputDim, int outputDim,float>
Matrix<stateDim, 1> Kalman<stateDim, inputDim, outputDim,float>::getStates() const {
    return X_hat_;
}