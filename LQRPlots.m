clc
close all

tempref=20;
co2ref=500;
N = length(out.InputNonConWithoutObs1(:,1));
x = 0:15:500;

%% Simulated input from the optimal controller without observer
figure('Position', [100, 100, 800, 400])

plot(x,out.InputNonConWithoutObs1(:,1),'LineWidth', 2, 'DisplayName', 'fan');
hold on
plot(x,out.InputNonConWithoutObs1(:,2),'LineWidth', 2, 'DisplayName', 'ECH1');
plot(x,out.InputNonConWithoutObs1(:,3),'LineWidth', 2, 'DisplayName', 'ECH2');
plot(x,out.InputNonConWithoutObs1(:,4),'LineWidth', 2, 'DisplayName', 'HVAC');
plot(x,out.InputNonConWithoutObs1(:,5),'LineWidth', 2, 'DisplayName', 'Bypass damper');
plot(x,out.InputNonConWithoutObs1(:,6),'LineWidth', 2, 'DisplayName', 'Outside temperature');
hold off
grid on
title("Simulated input from the optimal controller without observer")
ylabel("Inputs [%]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');

%% Simulated temperature from the optimal controller without observer
steady_state = mean(out.OutputNonConWithoutObs(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputNonConWithoutObs(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputNonConWithoutObs(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 25])
grid on
title("Simulated temperature output from the optimal controller without observer")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');


%% Simulated CO2 from the optimal controller without observer
steady_state = mean(out.OutputNonConWithoutObs(N-10:N,2));
steady_state_error = abs(steady_state-co2ref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputNonConWithoutObs(:,2) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputNonConWithoutObs(:,2),'LineWidth', 2, 'DisplayName', 'CO2');
yline(co2ref,':r','DisplayName', 'CO2 reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)

grid on
title("Simulated CO2 output from the optimal controller without observer")
ylabel("CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');



%% Simulated input from the optimal controller with observer
figure('Position', [100, 100, 800, 400])

plot(x,out.InputNonConWithObs(:,1),'LineWidth', 2, 'DisplayName', 'fan');
hold on
plot(x,out.InputNonConWithObs(:,2),'LineWidth', 2, 'DisplayName', 'ECH1');
plot(x,out.InputNonConWithObs(:,3),'LineWidth', 2, 'DisplayName', 'ECH2');
plot(x,out.InputNonConWithObs(:,4),'LineWidth', 2, 'DisplayName', 'HVAC');
plot(x,out.InputNonConWithObs(:,5),'LineWidth', 2, 'DisplayName', 'Bypass damper');
plot(x,out.InputNonConWithObs(:,6),'LineWidth', 2, 'DisplayName', 'Outside temperature');
hold off
grid on
title("Simulated input from the optimal controller with observer")
ylabel("Inputs [%]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');

%% Simulated temperature from the optimal controller with observer
steady_state = mean(out.OutputNonConWithObs(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputNonConWithObs(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputNonConWithObs(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 25])
grid on
title("Simulated temperature output from the optimal controller with observer")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');


%% Simulated CO2 from the optimal controller with observer
steady_state = mean(out.OutputNonConWithObs(N-10:N,2));
steady_state_error = abs(steady_state-co2ref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputNonConWithObs(:,2) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputNonConWithObs(:,2),'LineWidth', 2, 'DisplayName', 'CO2');
yline(co2ref,':r','DisplayName', 'CO2 reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)

grid on
title("Simulated CO2 output from the optimal controller with observer")
ylabel("CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');



%% Simulated input from the optimal controller with observer and constraints
figure('Position', [100, 100, 800, 400])

plot(x,out.InputConWithObs1(:,1),'LineWidth', 2, 'DisplayName', 'fan');
hold on
plot(x,out.InputConWithObs1(:,2),'LineWidth', 2, 'DisplayName', 'ECH1');
plot(x,out.InputConWithObs1(:,3),'LineWidth', 2, 'DisplayName', 'ECH2');
plot(x,out.InputConWithObs1(:,4),'LineWidth', 2, 'DisplayName', 'HVAC');
plot(x,out.InputConWithObs1(:,5),'LineWidth', 2, 'DisplayName', 'Bypass damper');
plot(x,out.InputConWithObs1(:,6),'LineWidth', 2, 'DisplayName', 'Outside temperature');
hold off
grid on
title("Simulated input from the optimal controller with observer and constraints")
ylabel("Inputs [%]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');

%% Simulated temperature from the optimal controller with observer
steady_state = mean(out.OutputConWithObs(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputConWithObs(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputConWithObs(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 25])
grid on
title("Simulated temperature output from the optimal controller with observer and constraints")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');


%% Simulated CO2 from the optimal controller with observer and constraints
steady_state = mean(out.OutputConWithObs(N-10:N,2));
steady_state_error = abs(steady_state-co2ref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputNonConWithObs(:,2) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputConWithObs(:,2),'LineWidth', 2, 'DisplayName', 'CO2');
yline(co2ref,':r','DisplayName', 'CO2 reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)

grid on
title("Simulated CO2 output from the optimal controller with observer and constraints")
ylabel("CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');
