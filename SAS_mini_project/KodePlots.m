close all
% Open the file for reading
[matrix1,matrix2,matrix3]=read("capture.txt");
[matrix1_1,matrix2_1,matrix3_1]=read("capteure.txt");


figure('Renderer', 'painters', 'Position', [10 10 1600 800])
time = (0:length(matrix1(:,1))-1) / 2; % Time vector based on sampling frequency of 2 Hz
plot(time,matrix1(:,1),'.-', 'LineWidth', 1.5,"DisplayName","Kalman Filtered States");
hold on
plot(time,matrix2(:,1),'.-', 'LineWidth', 1.5,"DisplayName","Kalman Predicted States")
plot(time,matrix3(:,1),'.-', 'LineWidth', 1.5,"DisplayName","Raw measurements")
title("Lattitude")
xlabel('Time [s]');
ylabel('Lattitude [m]');

legend()
hold off
saveas(gcf, 'lattitude_plot.png')



figure('Renderer', 'painters', 'Position', [10 10 1600 800])

time = (0:length(matrix1(:,1))-1) / 2; % Time vector based on sampling frequency of 2 Hz
plot(time,matrix1(:,2),'.-', 'LineWidth', 1.5,"DisplayName","Kalman Filtered States");
hold on
plot(time,matrix2(:,2),'.-', 'LineWidth', 1.5,"DisplayName","Kalman Predicted States")
plot(time,matrix3(:,2),'.-', 'LineWidth', 1.5,"DisplayName","Raw measurements")
xlabel('Time [s]');
ylabel('Lattitude [m]');
title("Longitude")
legend()
hold off
saveas(gcf, 'longitude_plot.png')

% Assuming you have the position data in matrix1(:,1), matrix1(:,2), matrix1_1(:,1), matrix1_1(:,2)
% and the speed data in matrix(:,3) and matrix(:,4)

% Create a new figure window for position plot
figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
% Position plot
hold on;
plot(matrix1_1(:,1), matrix1_1(:,2), 'x-', 'LineWidth', 1.5);
plot(matrix2_1(:,1), matrix2_1(:,2), 'x-', 'LineWidth', 1.5);
plot(matrix3_1(:,1), matrix3_1(:,2), 'x-', 'LineWidth', 1.5);
ylim([6346755,6346780])
xlim([605245,605297])
hold off;
title('Position Plot');
xlabel('X-position [m]');
ylabel('Y-position [m]');
legend('Updated states', 'Predicted states','Raw measurements');
grid on;

saveas(gcf, 'position_plot_kalmancompare.png')

% Create a new figure window for speed in x-direction
figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
% Speed in x-direction
time = (0:length(matrix1(:,3))-1) / 2; % Time vector based on sampling frequency of 2 Hz
time2 = (0:length(matrix1_1(:,3))-1) / 2; % Time vector based on sampling frequency of 2 Hz

plot(time, matrix1(:,3), 'b-', 'LineWidth', 1.5);
hold on;
plot(time2+time(end), matrix1_1(:,3), 'r-', 'LineWidth', 1.5);
hold off;
title('Speed in X-direction');
xlabel('Time [s]');
ylabel('Speed [m/s]');
legend('Speed 1', 'Speed 2');
grid on;
saveas(gcf, 'speed_x_plot.png')

% Create a new figure window for speed in y-direction
figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
% Speed in y-direction
time = (0:length(matrix1(:,3))-1) / 2; % Time vector based on sampling frequency of 2 Hz
time2 = (0:length(matrix1_1(:,3))-1) / 2; % Time vector based on sampling frequency of 2 Hz
plot(time, matrix1(:,4), 'b-', 'LineWidth', 1.5);
hold on;
plot(time2+time(end), matrix1_1(:,4), 'r-', 'LineWidth', 1.5);
hold off;
title('Speed in Y-direction');
xlabel('Time [s]');
ylabel('Speed [m/s]');
legend('Speed 1', 'Speed 2');
grid on;
saveas(gcf, 'speed_y_plot.png')

% Create a new figure window for combined position and speed plot
figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
% Combined position and speed plot
hold on;
% Combine position and speed vectors
quiver(matrix1(:,1), matrix1(:,2), matrix1(:,3), matrix1(:,4), 'b');
quiver(matrix1_1(:,1), matrix1_1(:,2), matrix1_1(:,3), matrix1_1(:,4), 'r');
hold off;
title('Combined Position and Speed Plot');
xlabel('X-position [m]');
ylabel('Y-position [m]');
legend('Position 1 + Speed', 'Position 2 + Speed');
grid on;
axis equal;
saveas(gcf, 'combined_position_speed_plot.png')

figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
% Combined position and speed plot
hold on;
% Combine position and speed vectors
quiver(matrix1(:,1), matrix1(:,2), matrix1(:,3), matrix1(:,4), 'b');
quiver(matrix1_1(:,1), matrix1_1(:,2), matrix1_1(:,3), matrix1_1(:,4), 'r');
hold off;
title('Combined Position and Speed Plot');
xlabel('X-position [m]');
ylabel('Y-position [m]');
legend('Position 1 + Speed', 'Position 2 + Speed');
grid on;
axis equal;
saveas(gcf, 'combined_position_speed_plot.png')

figure('Renderer', 'painters', 'Position', [10 10 1600 800]);
yyaxis left;
plot(time, matrix1(:,3), '-',"Color","#0072BD", 'LineWidth', 1.5);
hold on;
plot(time, matrix2(:,3), '--',"Color","#0072BD", 'LineWidth', 1.5);
ylabel('Speed [m/s]');
title('Speed and Acceleration in X-direction');
xlabel('Time [s]');
limy=ylim();
xlim([0,161.5])
grid on;
yyaxis right;
plot(time, matrix1(:,5), '-',"Color","#D95319", 'LineWidth', 1.5);
plot(time, matrix2(:,5), '--',"Color","#D95319", 'LineWidth', 1.5);
ylim(limy);
xlim([0,161.5])
ylabel('Acceleration [m/s^2]');
legend('Updated speed', 'Predicted speed', 'Updated acceleration', 'Predicted acceleration', 'Location', 'best');
saveas(gcf, 'speed_acceleration_update_predict.png');



plot(time, matrix1(:,3), 'b-', 'LineWidth', 1.5);
hold on;
plot(time2+time(end), matrix1_1(:,3), 'r-', 'LineWidth', 1.5);
hold off;
title('Speed in X-direction');
xlabel('Time [s]');
ylabel('Speed [m/s]');
legend('Speed 1', 'Speed 2');
grid on;
saveas(gcf, 'speed_x_plot.png')


figure('Renderer', 'painters', 'Position', [10 10 1600 800]);

plot(time, matrix1(:,9), '-', 'LineWidth', 1.5);
hold on;
plot(time, matrix2(:,9), '-', 'LineWidth', 1.5);
plot(time, matrix2(:,5), '-', 'LineWidth', 1.5);

hold off;
title('Heading');
xlabel('Time [s]');
ylabel('Speed [m/s]');
legend('Update 1', 'Pred',"Raw");
grid on;
saveas(gcf, 'speed_x_plot.png')

function [matrix1,matrix2,matrix3]=read(file)
fid = fopen(file, 'rt');
if fid == -1
        error('File cannot be opened: %s', file);
    end

    % Initialize three cell arrays to hold the data
    array1 = {};
    array2 = {};
    array3 = {};
    rowIndex = 1;

    % Read the file line by line
    while ~feof(fid)
        line = fgetl(fid);
        if ischar(line) && ~isempty(line)
            % Convert the string of numbers to a numeric array
            numericData = sscanf(line, '%f,', [1, inf]);

            % Determine which array to put the data based on rowIndex
            switch mod(rowIndex, 3)
                case 1
                    array1{end + 1} = numericData;
                case 2
                    array2{end + 1} = numericData;
                case 0
                    array3{end + 1} = numericData;
            end
            
            rowIndex = rowIndex + 1;
        end
    end

    % Close the file
    fclose(fid);
cellArray=array1;

maxLength = max(cellfun(@length, cellArray));

% Initialize the matrix with NaNs
matrix1 = NaN(length(cellArray), maxLength);

% Fill the matrix with data from the cell array
for i = 1:length(cellArray)
    currentLength = length(cellArray{i});
    matrix1(i, 1:currentLength) = cellArray{i};
end

cellArray=array2;

maxLength = max(cellfun(@length, cellArray));

% Initialize the matrix with NaNs
matrix2 = NaN(length(cellArray), maxLength);

% Fill the matrix with data from the cell array
for i = 1:length(cellArray)
    currentLength = length(cellArray{i});
    matrix2(i, 1:currentLength) = cellArray{i};
end

cellArray=array3;

maxLength = max(cellfun(@length, cellArray));

% Initialize the matrix with NaNs
matrix3 = NaN(length(cellArray), maxLength);

% Fill the matrix with data from the cell array
for i = 1:length(cellArray)
    currentLength = length(cellArray{i});
    matrix3(i, 1:currentLength) = cellArray{i};
end


end