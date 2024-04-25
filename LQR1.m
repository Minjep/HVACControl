sys = load('system.mat');
sys_100 = sys.sys_100_new

A = sys_100.A;
B = sys_100.B;
C = sys_100.C;
D = sys_100.D;
Ts = sys_100.Ts;

max_data = max(samletData_100_train);
u_new = table2array(samletData_100_train(:,inputNames));

% Normalize each row to range [0, 1]
min_u = table2array(minData(:,inputNames));
max_u = table2array(max_data(:,inputNames));

u_new_norm = (u_new - min_u) ./ (max_u - min_u);

%u_new = (u_new-min(u_new))/(max(u_new)-min(u_new))
t_new = 0:15:191789;

sys_cl = ss(A, B, C, D, Ts);
step(sys_cl)

[y_new, ~, x_new] = lsim(sys_cl, u_new_norm', t_new);


% Denormalize Y
max_y = table2array(max_data(:,outputNames));
min_y = table2array(minData(:,outputNames));

y_new2 = y_new .* (max_y - min_y) + min_y;

% Plot the output signals
figure;
subplot(2, 1, 1);
plot(t_new, y_new2(:, 1), 'b');  % Plot output 1
hold on;
plot(t_new, y_new2(:, 2), 'r');  % Plot output 2
xlabel('Time');
ylabel('Output');
title('Simulated Output Signals');
legend("t_ar","co2_ar");
grid on;
hold off;

% Plot the first input signal
subplot(2, 1, 2);
hold on;
plot(t_new, u_new(:,1)', 'b'); 
plot(t_new, u_new(:,2)', 'r');
plot(t_new, u_new(:,3)', 'g');
plot(t_new, u_new(:,4)', 'y');
plot(t_new, u_new(:,5)', 'm');
plot(t_new, u_new(:,6)', 'c');
plot(t_new, u_new(:,7)', 'k');
xlabel('Time');
ylabel('Input');
legend('rqf', 'rqt', 'ech\_1\_pct', 'ech\_2\_pct', 'hvac\_pct', 'damper\_bypass\_pos', 't\_ao', 'Location', 'best');
title('Input Signals');
grid on;
hold off;

%Checking observability and contrallability (should be equal to the number of states)
Ob = obsv(A,C);
rank(Ob)
Co = ctrb(A,B);
rank(Co)

%% 
close all
% Finding Q and R

n = numel(max_y');
Q = zeros(n, n);
for i = 1:n
   %Q(i, i) =1;
   %Q(i, i) =( 1 / (max_y(i)'^2));  % Set the diagonal entry based on max_y
end

Q=[0.00018, 0;
    0,0.00001];
  
disp('Diagonal Matrix Q:');
disp(Q);


Q_mark = C'*Q*C
%eig(Q_mark)


m = numel(max_u');
R = zeros(m, m);
for i = 1:m
    R(i, i) = 1 / (max_u(i)'^2);
    %R(i, i) = 1 ;  % Set the diagonal entry based on max_y
end
disp('Diagonal Matrix R:');
disp(R);

% R=diag(ones(7,1))
% Q_mark=diag(ones(20,1))
%Q_mark = C'*Q*C
%% 

% LQR gain matrix K
[K,P,~] = lqrd(A,B, Q_mark, R, Ts);
K_rf = inv(R+B'*P*B)*B'

disp('LQR Gain Matrix K:');
disp(K);

% Check stability
A_cl = A - B*K;
figure;
eigenvalues_cl = eig(A_cl);
plot(real(eigenvalues_cl), imag(eigenvalues_cl), 'rx', 'LineWidth', 2);
title('Eigenvalues of A_{cl} = A - BK');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;
%% 

sys_new = ss(A - B*K, B, C, D, Ts);
%step(sys_new)

ref = zeros(2, 1000);
ref(1, :) = 20;
ref(2, :) = 500;

v=inv(eye(10)-A_cl')*C'*Q*ref;

u_rf = K_rf*v
t_new2 = 0:15:14999;

[y_new3, ~, x_new2] = lsim(sys_new, u_rf', t_new2);

y_new4 = y_new3 .* (max_y - min_y) + min_y;

% Plot the output signals
% figure;
% plot(t_new2, y_new4(:, 1), 'b');  % Plot output 1
% hold on;
% plot(t_new2, y_new4(:, 2), 'r');  % Plot output 2
% xlabel('Time');
% ylabel('Output');
% title('Simulated Output Signals');
% legend("t_ar","co2_ar");
% grid on;
% hold off;

% Steady-state value (final value) of the response
steady_state_value = y_new4(end, :);
steady_state_error = ref(:,1) - steady_state_value';

disp(['Steady-state error for Output 1: ', num2str(steady_state_error(1))]);
disp(['Steady-state error for Output 2: ', num2str(steady_state_error(2))]);

figure;
subplot(2, 1, 1);
plot(t_new2, y_new4(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output System - Output 1');
grid on;

subplot(2, 1, 2);
plot(t_new2, y_new4(:, 2), 'r', 'LineWidth', 2);  % Plot output 2
hold on;
yline(ref(2:2), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 2');
legend('Output 2', 'Reference');
title('Simulated Response of Multi-Output System - Output 2');
grid on;

%[ABAR,BBAR,CBAR,T,K1] = ctrbf(A,B,C);
%% Observer design 

y_ref_norm_temp = (ref(1:1) - min_y(1:1)) ./ (max_y(1:1) - min_y(1:1));
y_ref_norm_co2 = (ref(2:2) - min_y(:,2)) ./ (max_y(:,2) - min_y(:,2));

A_new = sys_new.A;
B_new = sys_new.B;
C_new = sys_new.C;
D_new = sys_new.D;

p=pole(sys_new);

L = place(A_new', C_new', p)';
v=inv(eye(10)-A_cl')*C'*Q;

At = [ A-B*K             B*K
       zeros(size(A))    A-L*C ];

Bt = [    B
       zeros(size(B)) ];

Ct = [ C    zeros(size(C)) ];

sys_obs= ss(At, Bt, Ct, 0, Ts);
%step(sys_obs)

[y_obs, ~, x_obs] = lsim(sys_obs, ref, t_new2);

y_obs_de_norm = y_obs .* (max_y - min_y) + min_y;

steady_state_value_obs = y_obs_de_norm(end, :);
steady_state_error_obs = ref(:,1) - steady_state_value_obs';

disp(['Steady-state error for Output 1 for observer: ', num2str(steady_state_error_obs(1))]);
disp(['Steady-state error for Output 2 for observer: ', num2str(steady_state_error_obs(2))]);

figure;
subplot(2, 1, 1);
plot(t_new2, y_obs_de_norm(:, 1), 'b', 'LineWidth', 2);  % Plot output 1
hold on;
yline(ref(1:1), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 1');
legend('Output 1', 'Reference');
title('Simulated Response of Multi-Output observer System - Output 1');
grid on;

subplot(2, 1, 2);
plot(t_new2, y_obs_de_norm(:, 2), 'r', 'LineWidth', 2);  % Plot output 2
hold on;
yline(ref(2:2), 'k--', 'LineWidth', 1.5);  % Plot reference input
xlabel('Time');
ylabel('Output 2');
legend('Output 2', 'Reference');
title('Simulated Response of Multi-Output observer System - Output 2');
grid on;