#ifndef GLOBAL_SETTINGS_H
#define GLOBAL_SETTINGS_H
        #include <BasicLinearAlgebra.h>
        namespace GlobalSettings
        {
            struct KalmanSettings2
            {
                static constexpr  int stateDim=10;
                static constexpr  int inputDim=0;
                static constexpr  int outputDim=6;
                static constexpr float Ts =0.5;
                const float phi_x = 0.9;
                const float phi_y = 0.9;
                const float phi_z = 0.9;
                const BLA::Matrix<stateDim, stateDim,float> A = {1,0,Ts,0,0,0,0,0,
                                                                0,1,0,Ts,0,0,0,0,
                                                                0,0,1,0,Ts,0,0,0,
                                                                0,0,0,1,0,Ts,0,0,
                                                                0,0,0,0,0,0,0,0,
                                                                0,0,0,0,0,0,0,0,
                                                                0,0,0,0,0,0,1,0,
                                                                0,0,0,0,0,0,0,0};

                const BLA::Matrix<outputDim, stateDim, float> C = { 1,0,0,0,0,0,0,0,0,0,
                                                                    0,1,0,0,0,0,0,0,0,0,
                                                                    0,0,0,0,0,0,1,0,0,0,
                                                                    0,0,0,0,0,0,0,1,0,0,  
                                                                    0,0,0,0,0,0,0,0,1,0,
                                                                    0,0,0,0,0,0,0,0,0,1};
                const BLA::Matrix<stateDim, stateDim, float> Q = {
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0.1, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0.1, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1
                                                                };
                const BLA::Matrix<outputDim, outputDim, float> R =
                                                 {2,0,0,0,0,0,
                                                    0,2,0,0,0,0,
                                                    0,0,0.6,0,0,0,
                                                    0,0,0,0.8,0,0,
                                                    0,0,0,0,0.5,0,
                                                    0,0,0,0,0,0.005};
                const BLA::Matrix<stateDim, stateDim, float>   P = {100,0,0,0,0,0,0,0,0,0,
                                                                    0,100,0,0,0,0,0,0,0,0,
                                                                    0,0,100,0,0,0,0,0,0,0,
                                                                    0,0,0,100,0,0,0,0,0,0,
                                                                    0,0,0,0,100,0,0,0,0,0,
                                                                    0,0,0,0,0,100,0,0,0,0,
                                                                    0,0,0,0,0,0,100,0,0,0,
                                                                    0,0,0,0,0,0,0,100,0,0,
                                                                    0,0,0,0,0,0,0,0,100,0,
                                                                    0,0,0,0,0,0,0,0,0,100};    
                const BLA::Matrix<stateDim, 1, float> initX =  {0, 0, 0, 0, 0, 0, 0,0,0, 0};
                const BLA::Matrix<stateDim, stateDim, float> initP = P;
                const BLA::Matrix<stateDim, stateDim, float> I = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                    0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                                                    0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
                                                    0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                                    0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                                    0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
                                                    0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                                                    0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                                                    0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 1};

            
            }; // struct KalmanSettings

            extern KalmanSettings2 kalmanSettings; //        
         } // namespace GlobalSettings

#endif // GLOBAL_SETTINGS_H