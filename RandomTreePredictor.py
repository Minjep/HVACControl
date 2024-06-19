from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Load the dataset
file_path = r"C:\Users\jeppe\Downloads\dataN4sid.csv"
data = pd.read_csv(file_path)

# Convert unixTime to datetime
data['unixTime'] = pd.to_datetime(data['unixTime'])

# Extract useful time features
data['hour'] = data['unixTime'].dt.hour
data['day'] = data['unixTime'].dt.day
data['month'] = data['unixTime'].dt.month
data['year'] = data['unixTime'].dt.year

# Drop the original unixTime column
data = data.drop(columns=['unixTime'])

# Define features and targets
X = data.drop(columns=['t_ar', 'co2_ar'])
y = data[['t_ar', 'co2_ar']]

# Add new features
X['last_co2'] = data['co2_ar'].shift(1)
X['last_temp'] = data['t_ar'].shift(1)

# Drop rows with missing values
X = X.dropna()
y = y.iloc[1:]

# Split the data into training and testing sets
test_size = int(len(X) * 0.2)
X_train = X[:-test_size]
X_test = X[-test_size:]
y_train = y[:-test_size]
y_test = y[-test_size:]

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestRegressor(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)
# Build the neural network model
model = Sequential([
    Dense(100, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(30, activation='relu'),  # Add another hidden layer with 16 neurons
    Dense(2)  # Output layer with 2 neurons for t_ar and co2_ar
])

# Compile the model
model.compile(optimizer='adam', loss='mean_absolute_percentage_error')  

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=100, validation_split=0.2, verbose=0)
 
# Make predictions
y_pred_nn = model.predict(X_test_scaled)

# Evaluate the model
mse_t_ar = mean_squared_error(y_test['t_ar'], y_pred[:, 0])
r2_t_ar = r2_score(y_test['t_ar'], y_pred[:, 0])
mse_co2_ar = mean_squared_error(y_test['co2_ar'], y_pred[:, 1])
r2_co2_ar = r2_score(y_test['co2_ar'], y_pred[:, 1])

results = {
    'MSE t_ar': mse_t_ar,
    'R2 t_ar': r2_t_ar,
    'MSE co2_ar': mse_co2_ar,
    'R2 co2_ar': r2_co2_ar
}
mse_co2_ar_nn = mean_squared_error(y_test['co2_ar'], y_pred_nn[:, 1])
r2_co2_ar_nn = r2_score(y_test['co2_ar'], y_pred_nn[:, 1])
mse_t_ar_nn = mean_squared_error(y_test['t_ar'], y_pred_nn[:, 0])
r2_t_ar_nn = r2_score(y_test['t_ar'], y_pred_nn[:, 0])



results
x=np.arange(len(y_test))
plt.figure(figsize=(16, 9))

# Subplot 1: True vs Predicted t_ar
plt.subplot(2, 1, 1)
plt.plot(x, y_test['t_ar'], 'o-', label='True')
plt.plot(x, y_pred[:, 0], 'x-', label='Predicted')
plt.xlabel('Sample')
plt.ylabel('t_ar')
plt.title('True vs Predicted t_ar MSE: {:.4f}, R2: {:.4f}'.format(mse_t_ar, r2_t_ar))
plt.legend()

# Subplot 2: True vs Predicted co2_ar
plt.subplot(2, 1, 2)
plt.plot(x, y_test['co2_ar'], 'o-', label='True')
plt.plot(x, y_pred[:, 1], 'x-', label='Predicted')
plt.xlabel('Sample')
plt.ylabel('co2_ar')
plt.title('True vs Predicted co2_ar MSE: {:.4f}, R2: {:.4f}'.format(mse_co2_ar, r2_co2_ar))
plt.legend()

plt.suptitle('Performance of Random Forest Regressor on Test Data\n', fontsize=16)
plt.tight_layout()

plt.savefig('true_vs_predicted.png')
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(x, y_test['t_ar'], 'o-', label='True')
plt.plot(x, y_pred_nn[:, 0], 'x-', label='Predicted')
plt.xlabel('Sample')
plt.ylabel('t_ar')
plt.title('True vs Predicted t_ar (Neural Network)\nMSE: {:.4f}, R2: {:.4f}'.format(mse_t_ar_nn, r2_t_ar_nn))


plt.figure(figsize=(10, 5))
plt.plot(x, y_test['co2_ar'], 'o-', label='True')
plt.plot(x, y_pred_nn[:, 1], 'x-', label='Predicted')
plt.xlabel('Sample')
plt.ylabel('co2_ar')
plt.title('True vs Predicted co2_ar (Neural Network)\nMSE: {:.4f}, R2: {:.4f}'.format(mse_co2_ar_nn, r2_co2_ar_nn))

plt.show()

