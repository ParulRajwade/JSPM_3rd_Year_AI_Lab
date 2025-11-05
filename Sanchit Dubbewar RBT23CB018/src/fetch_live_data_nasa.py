import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
import os

def fetch_live_data(lat=18.54, lon=73.85, days_back=45):
    """
    Fetch live NASA POWER rainfall data for the last `days_back` days (including today).
    We fetch 45 days to ensure we have at least 30 valid days after filtering out -999 values.
    The LSTM model requires 30 days of historical data for predictions.

    Parameters:
        lat (float): Latitude of location (default: Mumbai)
        lon (float): Longitude of location (default: Mumbai)
        days_back (int): Number of days of recent data to fetch (default: 45 to ensure 30+ valid days)

    Returns:
        pd.DataFrame: DataFrame with columns ['date', 'rainfall_mm']
    """

    # Date range: from days_back ago to today
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days_back-1)  # -1 to include today

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"📅 Fetching NASA POWER rainfall from {start_str} to {end_str}...")
    print(f"📍 Location: {lat}°N, {lon}°E")
    print(f"🎯 Target: Need at least 30 valid days for LSTM model")

    # NASA POWER endpoint
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?start={start_str}&end={end_str}"
        f"&latitude={lat}&longitude={lon}"
        f"&community=ag&parameters=PRECTOTCORR"
        f"&format=JSON"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"❌ NASA API request failed: {e}")

    data = response.json()

    # Extract dates and rainfall in mm/day
    daily_data = data["properties"]["parameter"]["PRECTOTCORR"]
    dates = list(daily_data.keys())
    rainfall_mm = list(daily_data.values())

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "rainfall_mm": rainfall_mm
    })

    # Remove invalid entries (-999 values) and sort by date
    df = df[df["rainfall_mm"] != -999.0].sort_values("date").reset_index(drop=True)
    
    if df.empty:
        raise Exception("❌ No valid rainfall data received from NASA API")
    
    # Check if we have enough data for LSTM model
    if len(df) < 30:
        raise Exception(f"❌ Insufficient data for LSTM model. Need 30 days, got {len(df)} valid days. NASA may not have data for this location/date range.")
    
    # Use only the last 30 days for LSTM input (most recent data)
    if len(df) > 30:
        df = df.tail(30).reset_index(drop=True)
        print(f"📊 Using last 30 days from {len(df)} available days")

    # Ensure output folder exists
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/live_input.csv", index=False)

    print(f"✅ NASA rainfall data processed: {len(df)} valid days")
    print(f"📊 Data range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"🌧️ Rainfall range: {df['rainfall_mm'].min():.2f} to {df['rainfall_mm'].max():.2f} mm/day")
    print(f"🎯 Ready for LSTM model (30 days required, {len(df)} days available)")
    
    return df


if __name__ == "__main__":
    # For standalone testing
    fetch_live_data()
