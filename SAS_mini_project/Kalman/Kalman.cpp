#include<Kalman.h>

template <int stateDim, int inputDim, int outputDim>
Kalman<stateDim, inputDim, outputDim>::Kalman(const Matrix<stateDim, stateDim>& A,
                                              const Matrix<outputDim, stateDim>& C,
                                              const Matrix<stateDim, stateDim>& Q,
                                              const Matrix<outputDim, outputDim>& R,
                                              const Matrix<outputDim, stateDim>& P)
    : A_(A), C_(C), Q_(Q), R_(R), P_(P), I_(Matrix<outputDim, outputDim>::Identity()) {}

template <int stateDim, int inputDim, int outputDim>
void Kalman<stateDim, inputDim, outputDim>::init(const Matrix<stateDim, 1>& initX,
                                                 const Matrix<stateDim, stateDim>& initP, double dt) {
    X_hat_ = initX;
    P_ = initP;
    dt_ = dt;
}

template <int stateDim, int inputDim, int outputDim>
void Kalman<stateDim, inputDim, outputDim>::predict() {
    X_pred_ = A_ * X_hat_;
    Pp_ = A_ * P_ * ~A_ + Q_;
}

template <int stateDim, int inputDim, int outputDim>
void Kalman<stateDim, inputDim, outputDim>::update(const Matrix<stateDim, 1>& z) {
    K_ = P_ * ~C_ * (C_ * P_ * ~C_ + R_).Inverse();
    X_hat_ = X_pred_ + K_ * (z - C_ * X_pred_);
    P_ = (I_ - K_ * C_) * Pp_ * ~(I_ - K_ * C_) + K_ * R_ * ~K_;
}

template <int stateDim, int inputDim, int outputDim>
Matrix<stateDim, 1> Kalman<stateDim, inputDim, outputDim>::getStates() const {
    return X_hat_;
}