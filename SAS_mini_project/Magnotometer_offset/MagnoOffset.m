clc
clear
close all
data = load('magnoOffset.txt');
figure(1)
scatter(data(:,1),data(:,2));
hold on
scatter(data(:,1),data(:,3));
scatter(data(:,2),data(:,3));
 axis equal

meanX=mean(data(:,1));
meanY=mean(data(:,2));
meanZ=mean(data(:,3));

data(:,1) = data(:,1) -meanX;
data(:,2) = data(:,2) -meanY-5;
data(:,3) = data(:,3) -(meanZ);
figure(2)
scatter(data(:,1),data(:,2));
hold on
scatter(data(:,1),data(:,3));
scatter(data(:,2),data(:,3));
 axis equal