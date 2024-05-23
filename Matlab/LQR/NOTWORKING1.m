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
D=B*0;
% Timestep of the discrete system
dt = 15;

% Reference values
ref = [21; 500];

% Augment the system with integral action
n = size(A, 1);
m = size(B, 2);
p = size(C, 1);

Aaug = [A zeros(n, p); -C eye(p)];
Baug = [B; zeros(p, m)];
Caug = [C zeros(p, p)];

% Desired closed-loop pole locations (adjust as needed)
poles = [0.8 0.85 0.09 0.095];

% Design the state feedback gain matrix K
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

K_aug = dlqr(Aaug, Baug, Qn, R);
K_p = place(Aaug, Baug, poles);
K = K_aug;

% Extract the state feedback gain and integral gain
Kx = K(:, 1:n);
Ki = K(:, n+1:end);


% Observer design from Kx
sys_closed_Feedback=ss(A - B*Kx, B, C, D, 15);


observer_poles = 0.2*pole(sys_closed_Feedback);
L = place(A', C', observer_poles)';



% Calculate the feedforward gain using the augmented system
N = [A, B; C, zeros(p, m)];
Nbar = N \ [zeros(n, p); eye(p)];

Nx = Nbar(1:n, :);
Nu = Nbar(n+1:end, :);

% Simulation time
t = 0:dt:3000;
N = length(t);

% Pre-allocate storage for state, output, control input, and integral state
x = zeros(n, N);
y = zeros(p, N);
u = zeros(m, N);
x_aug = zeros(n + p, N);

% Initial state
x(:, 1) = zeros(n, 1);
x_aug(:, 1) = [x(:, 1); zeros(p, 1)];

% Manual simulation loop
for k = 1:N-1
    % Calculate control input
    u(:, k) = -Kx * x(:, k) - Ki * x_aug(n+1:end, k) + Nu * ref;
    
    % Update state
    x(:, k+1) = A * x(:, k) + Breal * (u(:, k)+[0;0;0;0;0;5]);
    
    % Update integral state
    x_aug(:, k+1) = [x(:, k); x_aug(3:4, k)] + [zeros(n,1);ref - C * x(:, k)];
    
    % Calculate output
    y(:, k) = C * x(:, k);
end

% Calculate final output
y(:, N) = C * x(:, N);

% Plot the output response
figure;
subplot(2, 1, 1);
plot(t, y);
hold on;
plot(t, repmat(ref(1), 1, N), '--', 'DisplayName', 'Reference 1');
plot(t, repmat(ref(2), 1, N), '--', 'DisplayName', 'Reference 2');
xlabel('Time');
ylabel('Output');
legend('Output 1', 'Output 2', 'Reference 1', 'Reference 2');
title('Closed-loop System Response with Feedforward and Integral Action');

% Plot the control input
subplot(2, 1, 2);
plot(t, u);
xlabel('Time');
ylabel('Control Input');
legend(arrayfun(@(i) sprintf('Control Input %d', i), 1:m, 'UniformOutput', false));
title('Control Input with Feedforward and Integral Action');
