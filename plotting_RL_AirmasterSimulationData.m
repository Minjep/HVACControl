clc
clear
close all
% Specify in the begining
file_path = '3.csv';
temperature_outside = 15;
%% load data or create filtered data file

str_temp = num2str(temperature_outside);
prefix = ['filtered_data_', str_temp];

% Check if any files with the specified prefix exist
file_list = dir([prefix, '*']);

if ~isempty(file_list)
    file_path = ['filtered_data_', str_temp, '.csv'];
    data= readmatrix(file_path);
else
    data_matrix = readmatrix(file_path);
    data_table = readtable(file_path);


    
    filtered_data_table = data_table(1:60:end, :);
    filtered_data_matrix = data_matrix(1:60:end, :);

    strings_column_3 = filtered_data_table{:, 3};

    damper_recirc_pos = zeros(size(strings_column_3));

    for i = 1:numel(strings_column_3)
        if startsWith(strings_column_3{i}, 'RC_STATE.VENT')
            damper_recirc_pos(i) = 0;
        elseif startsWith(strings_column_3{i}, 'RC_STATE.RECIRC')
            damper_recirc_pos(i) = 100;
        end
    end

    str = num2str(temperature_outside);
    filtered_data = [filtered_data_matrix, damper_recirc_pos];
    output_file_path=['filtered_data_', str_temp, '.csv'];
    
    % Write the filtered data to a new CSV file
    writematrix(filtered_data, output_file_path);
end


%%
data = data(121317:end,:);
iteration = data(:,1);
N = length(iteration);
target_room_temperature = data(1,4);
requested_flow = data(:,5);
requested_inlet_temperature = data(:,6);
temperature_room = data(:,8);
temperature_inlet = data(:,9);
co2_room=data(:,22);
damper_recirc_pos=data(:,24);
ech_1_pct = data(:,17);
ech_2_pct = data(:,18);
hvac_pct = data(:,20);

epsilon = zeros(N,1);
alpha = zeros(N,1);
Xi=0.9999;
temp=0;
for i=1:N
    epsilon(i) = 1*Xi^i;
    alpha(i) = 1*Xi^i;
    if alpha(i) < 0.0001 && temp == 0
        xline_Temp = i;
        temp=1;
    end
end

% calculate reward
rewards=zeros(N,3);
reward_sum=zeros(N,1);

for i=1:N
    rewards(i,1:2) = reward_function(temperature_room(i),co2_room(i));
    rewards(i,3) = (2*1.5*requested_flow(i) + 11.5*ech_1_pct(i) + 11.5*ech_2_pct(i) + 20*hvac_pct(i))*9/4600;
    reward_sum(i) = sum(rewards(i,:));
end


%% temperature room
figure('Position', [100, 100, 800, 400])
subplot(2, 1, 1);
plot(temperature_room);
title('Simulated room temperature with outside temperatue set to 15 °C');
%legend('Reward Sum');
%xline(xline_Temp,'r:','linewidth',2, 'HandleVisibility', 'off');
yline(target_room_temperature,'r:','linewidth',2)
ylabel("Room temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('Temperature room', 'target room temperature');


subplot(2, 1, 2);
plot(co2_room);
title('Simulated room CO2 concentration');
%legend('Reward Sum');
%xline(xline_Temp,'r:','linewidth',2, 'HandleVisibility', 'off');
ylabel("Room CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label


%%  temperature room with inputs
figure('Position', [100, 100, 800, 400])

plot(temperature_room);
hold on
plot(requested_inlet_temperature);

title('Room temperature with requested inlet temperature');
%xline(xline_Temp,'r:','linewidth',2);
yline(target_room_temperature,'r:','linewidth',2);
ylabel("Temperature [°C]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('Temperature room', 'Requested inlet temperature', 'Target room temperature');
%% CO2 room with input


figure('Position', [100, 100, 800, 400])
subplot(2, 1, 1);
plot(iteration(N-10000:N),co2_room(N-10000:N));
title('Simulated room CO2 concentration');
%legend('Reward Sum');
%xline(xline_Temp,'r:','linewidth',2, 'HandleVisibility', 'off');
%yline(target_room_temperature,'r:','linewidth',2)
ylabel("Room CO2 concentration [ppm]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label
legend('CO2 room');


subplot(2, 1, 2);
plot(iteration(N-10000:N),damper_recirc_pos(N-10000:N))
hold on
plot(iteration(N-10000:N),requested_flow(N-10000:N))
title('Recirculation inside damper position and requested flow');
%legend('Reward Sum');
%xline(xline_Temp,'r:','linewidth',2, 'HandleVisibility', 'off');
ylim([-5 100])
ylabel("Inputs [%]")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label

legend('Recirculation inside damper position','Requested flow');


%% simulated reward sum
figure('Position', [100, 100, 800, 400])
plot(reward_sum);
title('Simulated reward sum');
legend('Reward Sum');
%xline(xline_Temp,'r:','linewidth',2, 'HandleVisibility', 'off');
ylabel("Reward Sum")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label



%% individual rewards
figure('Position', [100, 100, 800, 400])
subplot(3, 1, 1);
plot(iteration(N-10000:N),rewards(N-10000:N,1));

title('Temperature reward');
%legend('Temperature reward');
%xline(xline_Temp,'r:','linewidth',2);
ylabel("Reward")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label

subplot(3, 1, 2);
plot(iteration(N-10000:N),rewards(N-10000:N,2));

title('CO2 Reward');
%legend('CO2 Reward');
%xline(xline_Temp,'r:','linewidth',2);
ylabel("Reward")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label

subplot(3, 1, 3);
plot(iteration(N-10000:N),rewards(N-10000:N,3));

title('Power Reward');
%legend('CO2 Reward');
%xline(xline_Temp,'r:','linewidth',2);
ylabel("Reward")
xlabel("Time [minutes]")
set(gca, 'FontSize', 12); % Change font size of ticks
set(get(gca, 'Title'), 'FontSize', 16); % Change font size of title
set(get(gca, 'XLabel'), 'FontSize', 14); % Change font size of x-axis label
set(get(gca, 'YLabel'), 'FontSize', 14); % Change font size of y-axis label






%% functions
function rewards = reward_function(temperature_room, CO2_room)
    % Define constants
    temperature_variance = 0.272; % based on airmaster data
    CO2_variance = 151.375; % based on airmaster data
    requested_room_temperature = 23;
    CO2_average_concentration_outside = 400;

    % Calculate temperature reward
    temperature_reward = -((temperature_room - requested_room_temperature) / temperature_variance) ^ 2;

    % Adjust CO2 concentration
    CO2_adjusted = max(CO2_average_concentration_outside, CO2_room);

    % Calculate CO2 reward
    CO2_reward = -((CO2_adjusted - CO2_average_concentration_outside) / CO2_variance) ^ 2;

    % Create array containing rewards
    rewards = [temperature_reward, CO2_reward];
end
