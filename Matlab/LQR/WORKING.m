close all
% Given matrices
A = [0.9133 -0.0786;
     0.2880  0.1446];
Breal = [-0.0007 -0.0003  0.0003 -0.0002 -0.0055 -0.0052;
      0.0015  0.0003 -0.0001 -0.0008  0.0316 -0.0009];
B = [-0.0007 -0.0003  0.0003 -0.0002 -0.0055 -0.0;
      0.0015  0.0003 -0.0001 -0.0008  0.0316 -0.000];

C = 1.0e+03 *[-0.0313  0.0004;
     -1.1418  0.7550];
sys = load("sysVentilation.mat");
sys = sys.sys;
A=sys.A;
Breal=sys.B;
C=sys.C;
% Timestep of the discrete system
dt = 15;

% Reference values
ref = [20; 500];

% Augment the system with integral action
n = size(A, 1);
m = size(B, 2);
p = size(C, 1);

Aaug = [A zeros(n, p); -C eye(p)];
Baug = [B; zeros(p, m)];
Caug = [C zeros(p, p)];

% Desired closed-loop pole locations (adjust as needed)
% Design the state feedback gain matrix K

% Design the state feedback gain matrix K
R = [0.0001*10, 0 , 0 , 0 , 0 , 0;
     0 , 0.0001*15 , 0 , 0 , 0 , 0;
     0 , 0 , 0.0001*15 , 0 , 0 , 0;
     0 , 0 , 0 , 0.0001*5, 0 , 0;
     0 , 0 , 0 , 0 , 0.0001, 0;
     0 , 0 , 0 , 0 , 0 , 0.0001*15];
Q = [1/0.5^2, 0;
     0,   1/50^2];
Qmark = C'*Q*C;

Qn = zeros(4,4);
Qn(1,1)=Qmark(1,1);
Qn(2,2)=Qmark(2,2);
Qn(1,2)=Qmark(1,2);
Qn(2,1)=Qmark(2,1);
Qn(3,3)=1;
Qn(4,4)=1;;
R = R;
K_aug=dlqr(Aaug,Baug,Qn,R);
%K_aug=place(Aaug,Baug,[0.1,0.15,0.3,0.35])
K=K_aug
% Extract the state feedback gain and integral gain
Kx = K(:, 1:n);
Ki = K(:, n+1:end);

% Create the closed-loop system
Acl = [A-B*Kx , -B*Ki; -C,eye(p)];
Bcl = [zeros(n, p);zeros(n, p); eye(p)];
Ccl = [C zeros(p, p) zeros(p, p)];
Dcl = zeros(p, p);
Acl = [A,-B*Kx,-B*Ki;
      L*C,A-L*C-B*Kx,-B*Ki;
      -C, zeros(p, n), eye(p)];
sys_cl = ss(Acl, Bcl, Ccl, Dcl, dt);

figure
pzmap(sys_cl)
title('Eigenvalues of closed loop with integral action');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;
saveas(gcf, 'Eigenvalues of integralLoop.png')

% Simulation time
t = 0:dt:3000;

% Reference input
r = repmat(ref, 1, length(t));
% Simulate the closed-loop system
[y, t, x] = lsim(sys_cl, r, t);

% Plot the output response
figure;
plot(t, y);
hold on;
plot(t, r, '--');
xlabel('Time');
ylabel('Output');
legend('Output 1', 'Output 2', 'Reference 1', 'Reference 2');
title('Closed-loop System Response');


N = length(y(:,1));
x = 0:15:(N-1)*15;
steady_state = mean(y(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((y(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,y(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 30])
grid on
title("Temperature output from the integal action controller without constraints")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');

