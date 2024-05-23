
clc
close all

tempref=20;
co2ref=500;
N = length(out.OutputIntegralActionSimp(:,1));
x = 0:15:(N-1)*15;
%% Experiment without constraints
N = length(out.simout(:,1));
x = 0:15:(N-1)*15;
steady_state = mean(out.simout(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.simout(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.simout(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 30])
grid on
title("Simulated temperature output from the integal action controller with observer without constraints")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');



%% Simulated input from the optimal controller with observer
figure('Position', [100, 100, 800, 400])

plot(x,out.InputIntegralActionSimp1(:,1),'LineWidth', 2, 'DisplayName', 'fan');
hold on
plot(x,out.InputIntegralActionSimp1(:,2),'LineWidth', 2, 'DisplayName', 'ECH1');
plot(x,out.InputIntegralActionSimp1(:,3),'LineWidth', 2, 'DisplayName', 'ECH2');
plot(x,out.InputIntegralActionSimp1(:,4),'LineWidth', 2, 'DisplayName', 'HVAC');
plot(x,out.InputIntegralActionSimp1(:,5),'LineWidth', 2, 'DisplayName', 'Bypass damper');
plot(x,out.InputIntegralActionSimp1(:,6),'LineWidth', 2, 'DisplayName', 'Outside temperature');
hold off
grid on
title("Simulated integral input from the integal action controller with observer")
ylabel("Inputs [%]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');

%% Simulated temperature from the optimal controller with observer
steady_state = mean(out.OutputIntegralActionSimp(N-10:N,1));
steady_state_error = abs(steady_state-tempref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputIntegralActionSimp(:,1) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputIntegralActionSimp(:,1),'LineWidth', 2, 'DisplayName', 'Temperature');
yline(tempref,':r','DisplayName', 'Temperature reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)
ylim([0 30])
grid on
title("Simulated temperature output from the integal action controller with observer")
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');


%% Simulated CO2 from the optimal controller with observer
steady_state = mean(out.OutputIntegralActionSimp(N-10:N,2));
steady_state_error = abs(steady_state-co2ref);
fprintf('steady state error: %d\n', steady_state_error);
% Calculate deviation from steady state for each variable
deviation = abs((out.OutputIntegralActionSimp(:,2) - steady_state) ./ steady_state);
% Find indices where deviation exceeds 5%
indices = find(deviation > 0.02);
% Find the last occurrence of these indices
last_index = indices(end);
settling_time = last_index*15;
fprintf('settling time in minutes(2 percent): %d\n', settling_time);

figure('Position', [100, 100, 800, 400])
plot(x,out.OutputIntegralActionSimp(:,2),'LineWidth', 2, 'DisplayName', 'CO2');
yline(co2ref,':r','DisplayName', 'CO2 reference','LineWidth', 2)
yline(steady_state + (steady_state*0.02),':','DisplayName', '2 % deviation','LineWidth', 1)
yline(steady_state - (steady_state*0.02),':','LineWidth', 1, 'HandleVisibility', 'off')
settling_time_label = ['settling time: ', num2str(settling_time),' minutes'];
xline(settling_time,':','LineWidth', 2, 'DisplayName', settling_time_label)

grid on
title("Simulated CO2 output from the integal action controller with observer")
ylabel("CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('show');
