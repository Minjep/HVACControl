close all
% Load the system
sys = load("sysVentilation.mat");
sys = sys.sys;

% Define the weighting matrices
Q = [1/0.5^2, 0; 0, 1/50^2];
Qmark = sys.C' * Q * sys.C;

R = [0.0001*10, 0 , 0 , 0 , 0 , 0;
     0 , 0.0001*15 , 0 , 0 , 0 , 0;
     0 , 0 , 0.0001*15 , 0 , 0 , 0;
     0 , 0 , 0 , 0.0001*5, 0 , 0;
     0 , 0 , 0 , 0 , 0.0001, 0;
     0 , 0 , 0 , 0 , 0 , 0.0001*15];

K_feedbackOnly = dlqr(sys.A, sys.B, Q, R);

Qn = zeros(4,4);
Qn(1,1) = Qmark(1,1);
Qn(2,2) = Qmark(2,2);
Qn(1,2) = Qmark(1,2);
%%On(1,2)=0;
Qn(2,1) = Qmark(2,1);
%On(2,1)=0;
Qn(3,3) = 1/1000;
Qn(4,4) =1/1000
R=R
% Augmented system
A_aug = [sys.A, zeros(2); sys.C, ones(2)];
B_aug = [sys.B; zeros(2,6)];
C_aug = [sys.C, zeros(size(sys.C,1),2)];

% Check the rank of the controllability matrix
ctrb_rank = rank(ctrb(A_aug, B_aug));
disp(['Rank of the controllability matrix: ', num2str(ctrb_rank)]);

% Design the LQR controller
K_aug = dlqr(A_aug, B_aug, Qn, R);
K_F = K_aug(:, 1:2);
K_i = K_aug(:, 3:4);

phi = sys.A - sys.B * K_F;
dcGain = sys.C * inv(eye(size(sys.A)) - phi) * sys.B;

% Check if dcGain is invertible
if rank(dcGain*dcGain') < min(size(dcGain*dcGain'))
    error('dcGain matrix is singular or nearly singular');
end
% Udregning med feed forvard fra dc gain
phi = A_aug - B_aug * K_aug;
dcGain = C_aug * inv(eye(size(A_aug)) - phi) * B_aug;

M = dcGain' * inv(dcGain * dcGain');


% Least squares tilgang som i buogen 313
a_ls=[sys.A-eye(2),sys.B;
 sys.C,zeros(2,6)]
b_ls = [zeros(size(sys.A, 2), 2); eye(2)];
X = a_ls \ b_ls;
Nx=X(1:2,:);
Nu=X(3:8,:);
N_hat=Nu+K_F*Nx
M=N_hat



a_ls=[A_aug -eye(4),B_aug;C_aug,zeros(2,10)];
b_ls = [zeros(size(A_aug, 2), 2); eye(2)];
X = a_ls \ b_ls;
Nx=X(1:2,:);
Nu=X(3:8,:);
N_hat=Nu+K_feedbackOnly*Nx
M=N_hat


% Closed-loop system matrices
A_aug_cl = [sys.A - sys.B * K_F, -sys.B * K_i; -sys.C, ones(2)];
B_aug_cl = [sys.B*M;ones(2,2)];
C_aug_cl = [sys.C,zeros(2,2)];
D_aug_cl = [zeros(1,2);zeros(1,2)];


% Check the closed-loop poles
closed_loop_poles = eig(A_aug_cl);
disp('Closed-loop poles:');
disp(closed_loop_poles);

% Define the closed-loop system
sys_closed = ss(A_aug_cl, B_aug_cl, C_aug_cl, D_aug_cl,sys.Ts);

% Define the reference signal and time axis
ref = zeros(2, 100);
ref(1, :) = 20;
ref(2, :) = 1000;
timeaxis = 0:15:100*15;
timeaxis = timeaxis(1:end-1);

% Simulate the closed-loop system
[y_cl, ~, x_cl] = lsim(sys_closed, ref, timeaxis);

% Plot the response
figure;
plot(timeaxis, y_cl);
xlabel('Time');
ylabel('Output');
title('Closed-loop System Response');

% Steady-state value and error
steady_state_value = y_cl(end, :);
steady_state_error = ref(:, 1) - steady_state_value';
disp("System feedback Steady State Error");
disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);
disp(['Steady-state error for Output 2: ', num2str(steady_state_error(2))]);
