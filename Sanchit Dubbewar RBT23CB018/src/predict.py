import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Step 1: Load the trained LSTM model
model = load_model("models/lstm_model.h5")

# Step 2: Load test input (X_test) and actual output (y_test)
X_test = np.load("data/processed/X_test.npy")
y_test = np.load("data/processed/y_test.npy")

# Step 3: Predict on the test data
y_pred = model.predict(X_test)

# Step 4: Rebuild and fit scaler on full original data to invert predictions
df = pd.read_csv("data/processed/daily_rainfall_pune.csv")
scaler = MinMaxScaler()
scaler.fit(df[["rainfall_mm"]])  # fit on original scale, not test set

# Step 5: Invert scaling from [0,1] → actual mm
y_pred_actual = scaler.inverse_transform(y_pred)
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

# Step 6: Save results to CSV
results = pd.DataFrame({
    "actual_rainfall_mm": y_test_actual.flatten(),
    "predicted_rainfall_mm": y_pred_actual.flatten()
})
results.to_csv("outputs/predictions.csv", index=False)

# Step 7: Plot predictions vs actual (first 200 days)
plt.figure(figsize=(12, 4))
plt.plot(results["actual_rainfall_mm"][:200], label="Actual")
plt.plot(results["predicted_rainfall_mm"][:200], label="Predicted")
plt.title("Actual vs Predicted Rainfall (First 200 Days of Test Set)")
plt.xlabel("Days")
plt.ylabel("Rainfall (mm)")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/plots/rainfall_predictions.png")
plt.show()

# Step 8: Evaluate model
mae = mean_absolute_error(y_test_actual, y_pred_actual)
rmse = np.sqrt(mean_squared_error(y_test_actual, y_pred_actual))
r2 = r2_score(y_test_actual, y_pred_actual)

print(f"\n📊 Model Evaluation on Test Set:")
print(f"MAE  (Mean Absolute Error)      : {mae:.4f} mm")
print(f"RMSE (Root Mean Squared Error) : {rmse:.4f} mm")
print(f"R²    (Explained Variance)     : {r2:.4f}")