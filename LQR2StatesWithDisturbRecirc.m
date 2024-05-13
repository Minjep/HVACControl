clear all;
close all;
format shortG
digits(6)

sys=load("sysRecirculation.mat");
sys100=sys.sys;
sys=load("sysVentilation.mat");
sys0=sys.sys;

data=load("data100train.mat");
data100train=data.data_100_train;
data=load("data0train.mat");
data0train=data.data_0_train;

designSys=sys100;
designData=data100train;

numInputs=size(sys100.B,2);
numStates=size(sys100.A,1);
numOutputs=size(sys100.C,1);
%Q=[0.022, 0;
%    0,0.00001];

%designDataOutput = designData(:, [8]);
%for i = 1:numOutputs
%       Q_mark(i, i) = 1 / (max(designDataOutput{:,i})'^2);
%end
%Q_mark = [0.0017955     ,       0;
%             0   1.0628e-06]
specialC = designSys.C(1,:);
Q = (1/0.5^2)
Qmark = specialC'*Q*specialC;
disp('Diagonal Matrix Qmark:');
disp(Qmark);

invC=inv(designSys.C)
specialCinv = invC(1,:);
% R = zeros(numInputs, numInputs);
% for i = 1:numInputs
% %     %R(i, i) = 1 / (max(designData{:,i})'^2);
%      R(i, i) = 1 / (100^2)*1/10;
% %     %R(i, i) = 1 / (100^2)*1/10;
% %     %R(i, i) = 1 ;  % Set the diagonal entry based on max_y
% end

 R=[0.0001*10, 0 , 0 , 0 , 0 , 0;
     0 , 0.0001*15 , 0 , 0 , 0 , 0;
     0 , 0 , 0.0001*15 , 0 , 0 , 0;
     0 , 0 , 0 , 0.0001*5, 0 , 0;
     0 , 0 , 0 , 0 , 0.0001, 0;
     0 , 0 , 0 , 0 , 0 , 0.0001*15]*10;

disp('Diagonal Matrix R:');
disp(R);



%% Design LQR controller
specialB=designSys.B;
specialB(:,end)=[0;0]
specialD=designSys.D(1,:)
[K,P,eigenvalues_cl] = dlqr(designSys.A,specialB, Qmark, R);
K_manual=inv(R+specialB'*P*specialB)*specialB'*P*designSys.A;
N=inv(R+specialB'*P*specialB)*specialB';
Phi=designSys.A-specialB*K;
v=inv(eye(numStates)-Phi')*specialC'*Q;
N_ref=N*v;
disp('LQR Gain Matrix K:');
disp(K);

% Check stability
sys_closed=ss(designSys.A - specialB*K, specialB, specialC, specialD, designSys.Ts);
figure;
pzmap(sys_closed);
title('Eigenvalues of A_{cl} = A - BK');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;


% simulating the system
ref = zeros(1,1000);
ref(1,:) = 20;
%ref( 2,:) = 500;
u_ref = (N_ref*ref)';
timeaxis=0:15:1000*15;
timeaxis=timeaxis(1:end-1);
[y_cl, ~, x_cl] = lsim(sys_closed, u_ref, timeaxis);
steady_state_value = y_cl(end, :);
steady_state_error = ref(:,1) - steady_state_value';
disp("System feedback Steady State Error");

disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);



figure;
subplot(1, 1, 1);
plot(timeaxis, y_cl(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output System - Output 1');
grid on;


% Now design observer

% The observer should have the same poles as the closed-loop system (or faster)
% We will design the observer poles to be a bit faster than the closed-loop poles

observer_poles = 1*eigenvalues_cl;
L = place(designSys.A', specialC', observer_poles)';
disp('Observer Gain Matrix L:');
disp(L);

% Check stability of the observer
observer_A = designSys.A - L*specialC;
observer_eigenvalues = eig(observer_A);
sys_observer=ss(observer_A,designSys.B,specialC,specialD,designSys.Ts);
figure;
pzmap(sys_observer);
if all( abs(observer_eigenvalues) < 1 )
    disp('Observer is stable');
else
    disp('Observer is not stable');
end


% Simulate the observer

At = [ designSys.A-designSys.B*K, designSys.B*K
       zeros(size(designSys.A)),designSys.A-L*specialC ];

Bt = [designSys.B*N_ref
       zeros(size(designSys.B*N_ref)) ];

Ct = [ specialC    zeros(size(specialC)) ];

sys_withobs= ss(At, Bt, Ct, 0, designSys.Ts);

ref = zeros(1,1000);
ref(1,:) = 20;
u_ref = (ref)';
timeaxis=0:15:1000*15;
timeaxis=timeaxis(1:end-1);
[y_cl_obs, ~, x_cl_obs] = lsim(sys_withobs, u_ref, timeaxis);
steady_state_value = y_cl_obs(end, :);
steady_state_error = ref(:,1) - steady_state_value';
disp("System with observer Steady State Error");
disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);


figure;
subplot(1, 1, 1);
plot(timeaxis, y_cl_obs(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output System - Output 1');
grid on;
hold off;
%% Tuning

% Define weighting factors
Q_weights = 0:0.1:2; % Range for Q weighting factor
R_weights = 0:0.1:2; % Range for R weighting factor

% Initialize variables to store optimal values
min_error = Inf;
optimal_Q_weight = [];
optimal_R_weight = [];
error_values = [];

% Iterate through Q and R weights
for i = 1:length(Q_weights)
    for j = 1:length(R_weights)
        % Weight Q and R matrices
        weighted_Q = Q * Q_weights(i);
        weighted_R = R * R_weights(j);
        
        % Solve the discrete-time algebraic Riccati equation
        [~, ~, ~, E] = care(designSys.A, specialB, weighted_Q, weighted_R);
        
        % Calculate the steady-state error
        error = trace(inv(eye(size(designSys.A)) + specialB * E) * specialB);
        
        % Store error value
        error_values(i, j) = error;
        
        % Check if the error is lower than the current minimum
        if error < min_error
            min_error = error;
            optimal_Q_weight = Q_weights(i);
            optimal_R_weight = R_weights(j);
        end
    end
end

% Display optimal weighting factors and minimum steady-state error
disp(['Optimal Q weighting factor: ', num2str(optimal_Q_weight)]);
disp(['Optimal R weighting factor: ', num2str(optimal_R_weight)]);
disp(['Minimum steady-state error: ', num2str(min_error)]);

% Plot error surface
[Q_grid, R_grid] = meshgrid(Q_weights, R_weights);
surf(Q_grid, R_grid, error_values);
xlabel('Q Weighting Factor');
ylabel('R Weighting Factor');
zlabel('Steady-state Error');
title('Steady-state Error vs. Q and R Weighting Factors');

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