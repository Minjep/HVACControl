#ifndef KALMAN_H_
#define KALMAN_H_
#include <Arduino.h>
#include <BasicLinearAlgebra.h>
#include "GlobalSettings.h"
using namespace BLA;

template <int stateDim, int inputDim, int outputDim>
class Kalman {
public:
    Kalman(const Matrix<stateDim, stateDim,float>& A, const Matrix<outputDim, stateDim,float>& C,
           const Matrix<stateDim, stateDim,float>& Q, const Matrix<outputDim, outputDim,float>& R,
           const Matrix<stateDim,stateDim,float>& P, const Matrix<stateDim,stateDim,float>& I)
        : A_(A), C_(C), Q_(Q), R_(R), P_(P), I_(I) {
            
        }
    void initMatrices(const Matrix<stateDim, stateDim,float>& A, const Matrix<outputDim, stateDim,float>& C,
           const Matrix<stateDim, stateDim,float>& Q, const Matrix<outputDim, outputDim,float>& R,
           const Matrix<stateDim,stateDim,float>& P, const Matrix<stateDim,stateDim,float>& I){
               A_ = A;
               C_ = C;
               Q_ = Q;
               R_ = R;
               P_ = P;
               I_ = I;
           }

    void init(const Matrix<stateDim, 1,float>& initX, const Matrix<stateDim,stateDim,float>& initP, float dt) {
        X_hat_ = initX;
        P_ = initP;
        Pp_ = initP;
        dt_ = dt;
        
    }

    void predict() {
        
        X_pred_ = A_ * X_hat_;
        
        Pp_ = A_ * P_ * ~A_ + Q_;
       
    }

    void specialBpredict(const Matrix<stateDim, inputDim,float>& B, const Matrix<inputDim, 1,float>& u) {
        X_pred_ = A_ * X_hat_ + B * u;
        
        Pp_ = A_ * P_ * ~A_ + Q_;
      
    }
    void buildExtendedMatrices(){
        theta = X_hat_(8,0);
        accx_B = X_hat_(6,0);
        accy_B = X_hat_(7,0);
        float sin_theta= sin(theta);
        float cos_theta = cos(theta);
        F_ex = {1,0,dt_,0,0,0,0,0,0,0,
                0,1,0,dt_,0,0,0,0,0,0,
                0,0,1,0,dt_,0,0,0,0,0,
                0,0,0,1,0,dt_,0,0,0,0,
                0,0,0,0,0,0,cos_theta,sin_theta,-sin_theta*accx_B+cos_theta*accy_B,0,
                0,0,0,0,0,0,-sin_theta,cos_theta,-cos_theta*accx_B-sin_theta*accy_B,0,
                0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_x,0,0,0,
                0,0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_y,0,0,
                0,0,0,0,0,0,0,0,1,dt_,
                0,0,0,0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_z};
        A_ex = { 1,0,dt_,0,0,0,0,0,0,0,
                0,1,0,dt_,0,0,0,0,0,0,
                0,0,1,0,dt_,0,0,0,0,0,
                0,0,0,1,0,dt_,0,0,0,0,
                0,0,0,0,0,0,cos(theta),sin(theta),0,0,
                0,0,0,0,0,0,-sin(theta),cos(theta),0,0,
                0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_x,0,0,0,
                0,0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_y,0,0,
                0,0,0,0,0,0,0,0,1,dt_,
                0,0,0,0,0,0,0,0,0,GlobalSettings::kalmanSettings.phi_z};
    //Serial<< "theta = "<< theta << "\n";
    //Serial<< "cos(theta) = "<< cos(theta) << "\n";
    //Serial<< "sin(theta) = "<< sin(theta) << "\n";
    }
    void extended_predict() {
        buildExtendedMatrices();
        //Serial << "A_ex = " << A_ex << "\n";
        X_pred_ = A_ex * X_hat_;
        //Serial << "X_pred_ = " << X_pred_ << "\n";
        Pp_ = F_ex* P_ * ~F_ex + Q_;
        //Serial << "PP_ = " << Pp_ << "\n";
      
    }

    void update(const Matrix<outputDim, 1,float>& z) {
        //Serial<< "z i kalman = "<< z << "\n";
        K_ = Pp_ * ~C_ * Inverse(C_ * Pp_ * ~C_ + R_);


        X_hat_ = X_pred_ + K_ * (z - C_ * X_pred_);
        P_ = (I_ - K_ * C_) * Pp_ + K_ * R_ * ~K_;
        ////Serial<< "z ="<< z << "\n";
        ////Serial << "X_hat_ = " << X_hat_ << "\n";
        //Serial << "PP = " << Pp_ << "\n";
    }

    Matrix<stateDim, 1,float> getStates() const {
        return X_hat_;
    }
    Matrix<stateDim, 1,float> getPredicted() const {
        return X_pred_;
    }

    void printAllMatrices(){
    
        Serial << "A_ex = " << A_ex << "\n";
        Serial << "F_ex = " << F_ex << "\n";

    }
private:
    Matrix<stateDim, stateDim,float> A_;
    Matrix<outputDim, stateDim,float> C_;
    Matrix<stateDim, stateDim,float> Q_;
    Matrix<outputDim, outputDim,float> R_;
    Matrix<stateDim,stateDim,float> P_;
    Matrix<stateDim, stateDim,float> Pp_;
    Matrix<stateDim, 1,float> X_hat_;
    Matrix<stateDim, 1,float> X_pred_;
    Matrix<stateDim, outputDim,float> K_;
    Matrix<stateDim, stateDim,float> I_;
    BLA::Matrix<stateDim, stateDim,float> F_ex;
    BLA::Matrix<stateDim, stateDim,float> A_ex;
    float accx_B = 0.0;
    float accy_B = 0.0;
    float theta = 0.0;
    double dt_;
};
#endif // KALMAN_H_