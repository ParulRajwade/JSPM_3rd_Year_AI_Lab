import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# Load trained model
model = load_model("models/lstm_model.h5")

# Load original full rainfall data
df = pd.read_csv("data/processed/daily_rainfall_pune.csv", parse_dates=["date"])
df = df.sort_values("date")

# Fit the same MinMaxScaler
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[["rainfall_mm"]])

# Use last 30 days as the starting window
last_30_days = scaled[-30:].reshape(1, 30, 1)

predictions_scaled = []

# Predict 7 days ahead one by one
for _ in range(7):
    # Predict the next day
    next_day_scaled = model.predict(last_30_days)[0][0]
    predictions_scaled.append(next_day_scaled)

    # Slide window: remove first, add prediction
    new_window = np.append(last_30_days[:, 1:, :], [[[next_day_scaled]]], axis=1)
    last_30_days = new_window

# Convert predictions back to actual mm
predictions_scaled = np.array(predictions_scaled).reshape(-1, 1)
predictions_mm = scaler.inverse_transform(predictions_scaled).flatten()

# Generate dates for the next 7 days
last_date = df["date"].iloc[-1]
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)

# Create DataFrame of predictions
forecast_df = pd.DataFrame({
    "date": future_dates,
    "predicted_rainfall_mm": predictions_mm
})

# Save predictions
forecast_df.to_csv("outputs/predictions_next_7_days.csv", index=False)

# Plot forecast
plt.figure(figsize=(8, 4))
plt.plot(forecast_df["date"], forecast_df["predicted_rainfall_mm"], marker='o', linestyle='-')
plt.title("Predicted Rainfall for Next 7 Days")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/plots/rainfall_forecast_next_7_days.png")
plt.show()

#print forecast_df
print("Predictions for the next 7 days saved to 'outputs/predictions_next_7_days.csv' and plot saved as 'outputs/plots/rainfall_forecast_next_7_days.png'.")
