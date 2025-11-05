import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Step 1: Load raw data (skip metadata header)
df = pd.read_csv("data/raw/POWER_Point_Daily_19850101_20250101_018d53N_073d85E_LST.csv", skiprows=9)

# Step 2: Rename for clarity
df.columns = ["YEAR", "DOY", "rainfall_mm"]

# Step 3: Convert YEAR + DOY → full date
df["date"] = pd.to_datetime(df["YEAR"] * 1000 + df["DOY"], format="%Y%j")

# Step 4: Keep only the needed columns
df = df[["date", "rainfall_mm"]]
df = df.sort_values("date")

# Step 5: Normalize rainfall
scaler = MinMaxScaler()
scaled_rain = scaler.fit_transform(df[["rainfall_mm"]])
df["scaled_rain"] = scaled_rain

# Step 6: Create sequences
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i - window_size:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

window_size = 30
X, y = create_sequences(scaled_rain, window_size)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Step 7: Split into training and test sets (80/20)
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Step 8: Confirm
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)
print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# Save sequences for model script
np.save("data/processed/X_train.npy", X_train)
np.save("data/processed/y_train.npy", y_train)
np.save("data/processed/X_test.npy", X_test)
np.save("data/processed/y_test.npy", y_test)

# Save the scaler for later use
import joblib
joblib.dump(scaler, "models/scaler.pkl")
print("✅ Scaler saved to models/scaler.pkl")
