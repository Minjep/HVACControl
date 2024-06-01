clear all;
close all;
format shortG

sys=load("sysRecirculation.mat");
sys100=sys.sys;
sys=load("sysVentilation.mat");
sys0=sys.sys;

data=load("data100train.mat");
data100train=data.data_100_train;
data=load("data0train.mat");
data0train=data.data_0_train;
plots=0
designSys=sys0;
designData=data100train;

numInputs=size(sys100.B,2);
numStates=size(sys100.A,1);
numOutputs=size(sys100.C,1);

%Q=[0.022, 0;
%    0,0.00001];

%designDataOutput = designData(:, [8]);
%Q_mark = 1 / (max(designDataOutput{:,8})^2)
%for i = 1:numOutputs
%       Q_mark(i, i) = 1 / (max(designDataOutput{:,i})'^2);
%end
% Q_mark = [0.0017955     ,       0;
%              0   1.0628e-06]
% disp('Diagonal Matrix Q_mark:');
% disp(Q_mark);
% 
% 
% 
% Q = designSys.C'*Q_mark*designSys.C;
% disp('Diagonal Matrix Q:');
% disp(Q);

Q = [1/0.5^2, 0;
     0,   1/50^2]
Qmark = designSys.C'*Q*designSys.C;

% R = zeros(numInputs, numInputs);
% for i = 1:numInputs
%     %R(i, i) = 1 / (max(designData{:,i})'^2);
%     R(i, i) = 1 / (100^2);
%     %R(i, i) = 1 / (100^2)*1/10;
%     %R(i, i) = 1 ;  % Set the diagonal entry based on max_y
% end

 R=[0.0001*10, 0 , 0 , 0 , 0 , 0;
     0 , 0.0001*15 , 0 , 0 , 0 , 0;
     0 , 0 , 0.0001*15 , 0 , 0 , 0;
     0 , 0 , 0 , 0.0001*5, 0 , 0;
     0 , 0 , 0 , 0 , 0.0001, 0;
     0 , 0 , 0 , 0 , 0 , 0.0001*15];

disp('Diagonal Matrix R:');
disp(R);



% Design LQR controller
specialB=designSys.B;
specialB(:,end)=[0;0]
[K,P,eigenvalues_cl] = dlqr(designSys.A,specialB, Qmark, R);
K_manual=inv(R+specialB'*P*specialB)*specialB'*P*designSys.A;
N=inv(R+specialB'*P*specialB)*specialB';
Phi=designSys.A-specialB*K;
v=inv(eye(numStates)-Phi')*designSys.C'*Q;
N_ref=N*v;
disp('LQR Gain Matrix K:');
disp(K);



% Check stability
sys_closed=ss(designSys.A - designSys.B*K, specialB, designSys.C, designSys.D, designSys.Ts);
if plots
figure;
pzmap(sys_closed);
title('Eigenvalues of A_{cl} = A - BK');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;
end


% simulating the system
ref = zeros(numOutputs,1000);
ref(1,:) = 20;
ref( 2,:) = 500;
u_ref = (N_ref*ref)';
timeaxis=0:15:1000*15;
timeaxis=timeaxis(1:end-1);
[y_cl, ~, x_cl] = lsim(sys_closed, u_ref, timeaxis);
steady_state_value = y_cl(end, :);
steady_state_error = ref(:,1) - steady_state_value';
disp("System feedback Steady State Error");

disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);
disp(['Steady-state error for Output 2: ', num2str(steady_state_error(2))]);

if plots

figure;
subplot(2, 1, 1);
plot(timeaxis, y_cl(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output System - Output 1');
grid on;

subplot(2, 1, 2);
plot(timeaxis, y_cl(:, 2), 'r', 'LineWidth', 2);  % Plot output 2
hold on;
yline(ref(2:2), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 2');
legend('Output 2', 'Reference');
title('Simulated Response of Multi-Output System - Output 2');
grid on;
hold off;

end
% Now design observer

% The observer should have the same poles as the closed-loop system (or faster)
% We will design the observer poles to be a bit faster than the closed-loop poles

observer_poles = 0.5*eigenvalues_cl;
L = place(designSys.A', -designSys.C', observer_poles)';
disp('Observer Gain Matrix L:');
disp(L);

% Check stability of the observer
observer_A = designSys.A - L*designSys.C;
observer_eigenvalues = eig(observer_A);
sys_observer=ss(observer_A,designSys.B,designSys.C,designSys.D,designSys.Ts);
if plots

figure;
pzmap(sys_observer);
if all( abs(observer_eigenvalues) < 1 )
    disp('Observer is stable');
else
    disp('Observer is not stable');
end
end

% Simulate the observer

At = [ designSys.A , -designSys.B*K
       -L*designSys.C ,designSys.A+L*designSys.C ];

Bt = [specialB*N_ref
       zeros(size(designSys.B*N_ref)) ];

Ct = [ designSys.C    zeros(size(designSys.C)) ];

sys_withobs= ss(At, Bt, Ct, 0, designSys.Ts);

ref = zeros(numOutputs,1000);
ref(1,:) = 20;
ref( 2,:) = 500;
u_ref = (ref)';
timeaxis=0:15:1000*15;
timeaxis=timeaxis(1:end-1);
[y_cl_obs, ~, x_cl_obs] = lsim(sys_withobs, u_ref, timeaxis);
steady_state_value = y_cl_obs(end, :);
steady_state_error = ref(:,1) - steady_state_value';
disp("System with observer Steady State Error");
disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);
disp(['Steady-state error for Output 2: ', num2str(steady_state_error(2))]);

if plots

figure;
subplot(2, 1, 1);
plot(timeaxis, y_cl_obs(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output System - Output 1');
grid on;

subplot(2, 1, 2);
plot(timeaxis, y_cl_obs(:, 2), 'r', 'LineWidth', 2);  % Plot output 2
hold on;
yline(ref(2:2), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 2');
legend('Output 2', 'Reference');
title('Simulated Response of Multi-Output System - Output 2');
grid on;
hold off;
end


%% Integral
% Now we will design the integral action
% Take the poles of the closed-loop system and add a pole at the origin
% This will give us a stable system with integral action
% Write extended system
% do pole placement
% Extract the K and Ki from the extended system

A_ext = [designSys.A, zeros(numStates, numOutputs)
         designSys.C, eye(numOutputs, numOutputs)];
B_ext = [specialB
         zeros(numOutputs, numInputs)];
C_ext = [designSys.C, zeros(numOutputs, numOutputs)];
D_ext = designSys.D;
Qn=zeros(4);
Qn(1,1)=Qmark(1,1)
Qn(2,2)=Qmark(2,2)
Qn(1,2)=Qmark(1,2)
Qn(2,1)=Qmark(2,1)
Qn(3,3)=1;
Qn(4,4)=1/20;

K_ext = dlqr(A_ext,B_ext,Qn,R);

K_F = K_ext(:, 1:2);
Ki = K_ext(:, 3:4);
disp('Integral Gain Matrix Ki:');
disp(Ki);

 %% plots

% Constants and System Definitions
% Constants and System Definitions
ref = [20; 500];  % Step reference values for the outputs

% Define augmented system matrices
A_aug = [designSys.A - designSys.B*K - L*designSys.C, designSys.B*Ki;  % Controller and integral action
         designSys.C, zeros(numOutputs)];  % Observer
B_aug = [zeros(numStates, numOutputs); eye(numOutputs)];
C_aug = [designSys.C zeros(numOutputs)];

% Create the state-space model
sys_aug = ss(A_aug, B_aug, C_aug, zeros(numOutputs, numOutputs), designSys.Ts);

% Simulation settings
timeaxis=0:15:1000*15;
timeaxis=timeaxis(1:end-1);
u_ref = [zeros(numOutputs, 200), repmat(ref, 1, 800)];  % Step input after initial zero input

% Simulate
[y_aug, t_aug] = lsim(sys_aug, u_ref', timeaxis);

% Plot results
figure;
subplot(2, 1, 1);
plot(t_aug, y_aug(:, 1), 'b-', 'LineWidth', 2);
hold on;
plot(t_aug, u_ref(1, :), 'k--', 'LineWidth', 1.5);
title('Response with Observer and Integral Control - Output 1');
xlabel('Time (s)');
ylabel('Output 1');
legend('System Output', 'Reference');

subplot(2, 1, 2);
plot(t_aug, y_aug(:, 2), 'r-', 'LineWidth', 2);
hold on;
plot(t_aug, u_ref(2, :), 'k--', 'LineWidth', 1.5);
title('Response with Observer and Integral Control - Output 2');
xlabel('Time (s)');
ylabel('Output 2');
legend('System Output', 'Reference');

% Calculate and display steady-state errors
steady_state_error = ref - y_aug(end, :)';
disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);
disp(['Steady-state error for Output 2: ', num2str(steady_state_error(2))]);