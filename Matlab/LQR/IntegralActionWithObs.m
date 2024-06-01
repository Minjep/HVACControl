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


% Define timestep
dt = 15;

% Augment the system with integral action
n = size(A, 1);
m = size(Breal, 2);
p = size(C, 1);

Aaug = [A zeros(n, p); -C eye(p)];
Baug = [B; zeros(p, m)];
Caug = [C zeros(p, p)];

% Define the weighting matrices Q and R
% Adjust these values to ensure they are appropriate for your system
R = [0.0001*15, 0 , 0 , 0 , 0 , 0;
     0 , 0.0001*15 , 0 , 0 , 0 , 0;
     0 , 0 , 0.0001*15 , 0 , 0 , 0;
     0 , 0 , 0 , 0.0001*15, 0 , 0;
     0 , 0 , 0 , 0 , 0.0001*15, 0;
     0 , 0 , 0 , 0 , 0 , 0];
Q = [1/0.5^2, 0;
     0,   1/50^2];
Qmark = C'*Q*C;

Qn = zeros(4,4);
Qn(1,1)=Qmark(1,1);
Qn(2,2)=Qmark(2,2);
Qn(1,2)=Qmark(1,2);
Qn(1,2)=0;
Qn(2,1)=Qmark(2,1);
Qn(2,1)=0;
Qn(3,3)=10;
Qn(4,4)=1;
R = R*100;
% Calculate the state feedback gain matrix K
[K_aug, ~, ~] = dlqr(Aaug, Baug, Qn, R);

% Extract the state feedback gain and integral gain
Kx = K_aug(:, 1:n);
Ki = K_aug(:, n+1:end);

% Define the closed-loop A matrix
sys_closed_Feedback=ss(A - B*Kx, B, C, D, 15);


observer_poles = 0.2*pole(sys_closed_Feedback);
L = place(A', -C', observer_poles)';

% Display observer gain matrix
disp('Observer Gain Matrix L:');
disp(L);

% Create the closed-loop system matrices
    
    Acl = [A, -Breal*Kx, -Breal * Ki;
           -L*C,A + L * C, zeros(n, p);
           -C,zeros(p, n),eye(p)];
    Bcl = [zeros(n, p); zeros(n, p); eye(p)];
    Ccl = [C zeros(p, n) zeros(p, p)];
    Dcl = zeros(p, p);


% Create state-space model for closed-loop system
sys_cl = ss(Acl, Bcl, Ccl, Dcl, dt);

% Plot the pole-zero map
figure;
pzmap(sys_cl);
title('Eigenvalues of system with integral action');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;
axis equal;
saveas(gcf, 'Eigenvalues_of_integralLoop.png');

% Check stability
if all(real(eig(Acl)) < 0)
    disp('The system is stable.');
else
    disp('The system is unstable.');
end


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

