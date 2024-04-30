// pseudo code for project


// Start by setting up all sensors and kalman filter parameters


// Run GNNS initialization where the current position is set as the origin and then meters from the origin are calculated

// Get the current position from the GNSS sensor
// 
// Get the current acceleration from the IMU sensor
// Get the current angular velocity from the gyro sensor
// Get the heading from the magnetometer (maybe use as input)

// Use the Kalman filter for sensor fusion to get the current position and velocity
// First do the prediction step using the acceleration and angular velocity and heading
// Then do the update step using the GNSS position (meter from origin) 

// Display the current position and velocity on the serial monitor

w 
