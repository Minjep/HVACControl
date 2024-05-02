clc
clear
close all
data = load('magnoVariance.txt');

mean1 = mean(data(:,1));
mean2 = mean(data(:,2));
mean3 = mean(data(:,3));

var(data(:,1))
var(data(:,2))
var(data(:,3))

% Create a figure
figure;

% Create subplot 1
subplot(3, 1, 1); % 3 rows, 1 column, first subplot
plot(data(:,1));
yline(mean1,'linewidth',2);
xlim([0 1632])
title('Magnetfelt i x-retning [muT]');

% Create subplot 2
subplot(3, 1, 2); % 3 rows, 1 column, second subplot
plot(data(:,2));
yline(mean2,'linewidth',2);
xlim([0 1632])
title('Magnetfelt i y-retning [muT]');

% Create subplot 3
subplot(3, 1, 3); % 3 rows, 1 column, third subplot
plot(data(:,3));
yline(mean3,'linewidth',2);
xlim([0 1632])
title('Magnetfelt i z-retning [muT]');