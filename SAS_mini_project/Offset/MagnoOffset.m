clc
clear
close all
data = load('magnoOffset.txt');
figure(1)
scatter(data(:,1),data(:,2));
hold on
scatter(data(:,1),data(:,3));
scatter(data(:,2),data(:,3));
xline(0);
yline(0);
 axis equal

meanX=mean(data(:,1));
meanY=mean(data(:,2));
meanZ=mean(data(:,3));
legend('Bx, By', 'Bx, Bz','By, Bz');

data(:,1) = data(:,1) -meanX-2;
data(:,2) = data(:,2) -meanY-5;
data(:,3) = data(:,3) -(meanZ);
figure(2)
scatter(data(:,1),data(:,2));
hold on
scatter(data(:,1),data(:,3));
scatter(data(:,2),data(:,3));
legend('Bx, By', 'Bx, Bz','By, Bz');
xline(0);
yline(0);
xlim([-50, 50]); % Set x-axis limits from -50 to 50
ylim([-50, 50]); % Set y-axis limits from -1.2 to 1.2