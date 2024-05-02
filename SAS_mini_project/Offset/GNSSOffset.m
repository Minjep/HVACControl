clc
clear
close all
data = readmatrix('GNSSOffsetData.txt');
data(:,2:3)=data(:,2:3)*10^-7;

figure(1);
scatter(data(:,2),data(:,3));
axis equal

%% Data process
% Calculate mean values
latMean = mean(data(:,2));
longMean = mean(data(:,3));

% Set realLat and realLong to mean values
realLat = latMean;
realLong = longMean;

% Earth's radius in meters
R = 6371000;

% Preallocate matrix for distances in cm
distances_cm = zeros(size(data, 1), 2); % Each row will have lat and long distance in cm

for i = 1:size(data, 1)
    % Current point's coordinates
    lat = data(i, 2);
    long = data(i, 3);
    
    % Convert degrees to radians
    latRad = deg2rad(lat);
    longRad = deg2rad(long);
    realLatRad = deg2rad(realLat);
    realLongRad = deg2rad(realLong);
    
    % Differences in coordinates
    deltaLat = latRad - realLatRad;
    deltaLong = longRad - realLongRad;
    
    % Haversine formula for latitude distance
    a = sin(deltaLat/2)^2 + cos(realLatRad) * cos(latRad) * sin(0)^2;
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    latDist = R * c; % Latitude distance in meters
    
    % Haversine formula for longitude distance
    a = sin(0)^2 + cos(realLatRad) * cos(latRad) * sin(deltaLong/2)^2;
    c = 2 * atan2(sqrt(a), sqrt(1-a));
    longDist = R * c; % Longitude distance in meters
    
    % Determine the sign for latitudinal distance (-ve for south, +ve for north)
    latSign = sign(deltaLat);
    % Determine the sign for longitudinal distance (-ve for west, +ve for east)
    longSign = sign(deltaLong);
    
    % Apply signs to the distances and convert to cm
    distances_cm(i, 1) = latDist * latSign * 100; % Latitude distance in cm
    distances_cm(i, 2) = longDist * longSign * 100; % Longitude distance in cm
end

figure(2);
scatter(distances_cm(:,1),distances_cm(:,2));
axis equal
% Now distances_cm contains the latitudinal and longitudinal distances in cm
% from the realLat and realLong for each point
%% find meassures
stdPrec=std(distances_cm);

% Calculate the radial distances for each point
radial_distances = sqrt(sum(distances_cm.^2, 2));

% CEP - 50th percentile of the radial distances
CEP = prctile(radial_distances, 50);

% RMS - Root mean square of the radial distances
RMS = sqrt(mean(radial_distances.^2));

% 2DRMS - Twice the RMS value
twoDRMS = 2 * RMS;

% R95 - 95th percentile of the radial distances
R95 = prctile(radial_distances, 95);

mean(distances_cm)
figure(2);
scatter(distances_cm(:,1),distances_cm(:,2));
rectangle('Position', [-CEP, -CEP, 2*CEP, 2*CEP], ...
          'Curvature', [1, 1], ...
          'EdgeColor', 'r', 'LineWidth', 1, 'LineStyle', '--');

axis equal
