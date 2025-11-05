import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import joblib
import os
from datetime import datetime, timedelta

def generate_forecast(df, model_path="models/lstm_model.h5", scaler_path="models/scaler.pkl", days_to_predict=7):
    """
    Generate a rainfall forecast for the next `days_to_predict` days using a pre-trained LSTM model.
    The forecast starts from tomorrow (today + 1 day) to provide future predictions.

    Parameters:
        df (pd.DataFrame): DataFrame containing columns ['date', 'rainfall_mm']
        model_path (str): Path to saved LSTM model
        scaler_path (str): Path to saved scaler
        days_to_predict (int): Number of days to forecast

    Returns:
        pd.DataFrame: Forecast DataFrame with columns ['date', 'predicted_rainfall_mm']
    """

    # Validate input data
    if df.empty:
        raise ValueError("❌ Input DataFrame is empty")
    
    if 'date' not in df.columns or 'rainfall_mm' not in df.columns:
        raise ValueError("❌ Input DataFrame must have 'date' and 'rainfall_mm' columns")
    
    if len(df) < 30:
        raise ValueError(f"❌ Need at least 30 days of data, got {len(df)}")

    # Ensure output folders exist
    os.makedirs("outputs/plots", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Check if model files exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"❌ LSTM model not found at {model_path}")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"❌ Scaler not found at {scaler_path}")

    try:
        # Load model and scaler
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        raise Exception(f"❌ Failed to load model/scaler: {e}")

    # Sort and scale rainfall data
    df = df.sort_values("date").reset_index(drop=True)
    
    # Use last 30 days for prediction (LSTM input requirement)
    last_30_days = df.tail(30)
    scaled = scaler.transform(last_30_days[["rainfall_mm"]])
    
    # Reshape for LSTM: (samples, timesteps, features)
    last_30 = scaled[-30:].reshape(1, 30, 1)

    print(f"🔮 Generating {days_to_predict} day forecast using last 30 days of data...")
    print(f"📅 Last data date: {df['date'].iloc[-1].strftime('%Y-%m-%d')}")

    # Generate predictions
    predictions_scaled = []
    current_input = last_30.copy()
    
    for day in range(days_to_predict):
        next_day = model.predict(current_input, verbose=0)[0][0]
        predictions_scaled.append(next_day)
        # Update input for next prediction (shift window)
        current_input = np.append(current_input[:, 1:, :], [[[next_day]]], axis=1)

    # Inverse transform to mm
    predictions_scaled = np.array(predictions_scaled).reshape(-1, 1)
    predictions_scaled = np.clip(predictions_scaled, 0, 1)  # Ensure non-negative
    predictions_mm = scaler.inverse_transform(predictions_scaled).flatten()

    # Create forecast DataFrame starting from tomorrow
    today = datetime.now().date()
    start_date = today + timedelta(days=1)  # Start from tomorrow
    future_dates = pd.date_range(start=start_date, periods=days_to_predict)

    forecast_df = pd.DataFrame({
        "date": future_dates,
        "predicted_rainfall_mm": np.round(predictions_mm, 2)
    })

    # Save to CSV
    forecast_df.to_csv("outputs/predictions_next_7_days_on_NASA_data.csv", index=False)

    # Create enhanced plot
    plt.figure(figsize=(12, 6))
    
    # Plot historical data (last 7 days)
    historical_dates = df.tail(7)['date']
    historical_rainfall = df.tail(7)['rainfall_mm']
    plt.plot(historical_dates, historical_rainfall, 'b-o', linewidth=2, markersize=6, label='Historical (Last 7 days)')
    
    # Plot forecast
    plt.plot(forecast_df["date"], forecast_df["predicted_rainfall_mm"], 'r--o', linewidth=2, markersize=6, label='Forecast (Next 7 days)')
    
    plt.title("🌧️ Rainfall Forecast: Historical vs Predicted", fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Rainfall (mm/day)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plt.savefig("outputs/plots/rainfall_forecast_next_7_days_on_NASA_data.png", dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✅ Forecast generated for {days_to_predict} days starting from {start_date.strftime('%Y-%m-%d')}")
    print(f"📊 Forecast range: {forecast_df['date'].min().strftime('%Y-%m-%d')} to {forecast_df['date'].max().strftime('%Y-%m-%d')}")
    print(f"🌧️ Average predicted rainfall: {np.mean(predictions_mm):.2f} mm/day")
    
    return forecast_df


if __name__ == "__main__":
    # Standalone test: read from CSV
    try:
        df = pd.read_csv("data/processed/live_input.csv", parse_dates=["date"])
        generate_forecast(df)
    except Exception as e:
        print(f"❌ Error: {e}")
