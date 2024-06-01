clear all;
close all;
sys=load("sysRecirculation.mat");
sys100=sys.sys;
sys=load("sysVentilation.mat");
sys0=sys.sys;

data=load("data100train.mat");
data100train=data.data_100_train;
data=load("data0train.mat");
data0train=data.data_0_train;

designSys=sys0;
designData=data100train;

numInputs=size(sys100.B,2);
numStates=size(sys100.A,1);
numOutputs=size(sys100.C,1);
Q=[0.022, 0;
    0,0.00001];
disp('Diagonal Matrix Q:');
disp(Q);


Q_mark = designSys.C'*Q*designSys.C
disp('Diagonal Matrix Q_mark:');
disp(Q_mark);

R = zeros(numInputs, numInputs);
for i = 1:numInputs
    R(i, i) = 1 / (max(designData{:,i})'^2);
    %R(i, i) = 1 ;  % Set the diagonal entry based on max_y
end
disp('Diagonal Matrix R:');
disp(R);



%% Design LQR controller
[K,P,eigenvalues_cl] = dlqr(designSys.A,designSys.B, Q_mark, R);
K_manual=inv(R+designSys.B'*P*designSys.B)*designSys.B'*P*designSys.A;
N=inv(R+designSys.B'*P*designSys.B)*designSys.B';
Phi=designSys.A-designSys.B*K;
v=inv(eye(numStates)-Phi')*designSys.C'*Q;
N_ref=N*v;
disp('LQR Gain Matrix K:');
disp(K);

% Check stability
figure('Renderer', 'painters', 'Position', [10 10 1600 800])

sys_closed=ss(designSys.A - designSys.B*K, designSys.B, designSys.C, designSys.D, designSys.Ts);
figure;
pzmap(sys_closed);
title('Eigenvalues of A_{cl} = A - BK');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;
saveas(gcf, 'Eigenvalues of A_BK.png')


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


% Now design observer

% The observer should have the same poles as the closed-loop system (or faster)
% We will design the observer poles to be a bit faster than the closed-loop poles

observer_poles = 1.5*eigenvalues_cl;
L = place(designSys.A', designSys.C', observer_poles)';
disp('Observer Gain Matrix L:');
disp(L);

% Check stability of the observer
observer_A = designSys.A - L*designSys.C;
observer_eigenvalues = eig(observer_A);
sys_observer=ss(observer_A,designSys.B,designSys.C,designSys.D,designSys.Ts);
figure;
pzmap(sys_observer);
if all( abs(observer_eigenvalues) < 1 )
    disp('Observer is stable');
else
    disp('Observer is not stable');
end


% Simulate the observer

At = [ designSys.A-designSys.B*K, designSys.B*K
       zeros(size(designSys.A)),designSys.A-L*designSys.C ];

Bt = [designSys.B*N_ref
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


%% Integral
% Now we will design the integral action
% Take the poles of the closed-loop system and add a pole at the origin
% This will give us a stable system with integral action
% Write extended system
% do pole placement
% Extract the K and Ki from the extended system

PolesI = [eigenvalues_cl; 0.0009 ; 0.0009];
A_ext = [designSys.A, zeros(numStates, numOutputs)
         designSys.C, zeros(numOutputs, numOutputs)];
B_ext = [designSys.B
         zeros(numOutputs, numInputs)];
C_ext = [designSys.C, zeros(numOutputs, numOutputs)];
D_ext = designSys.D;
K_ext = place(A_ext, B_ext, PolesI);
K_F = K_ext(1:numInputs, 1:2);
Ki = K_ext(1:numInputs, 3:4);
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