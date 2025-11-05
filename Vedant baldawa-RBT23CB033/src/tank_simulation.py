import pandas as pd

def simulate_tank_levels(
    merged_df,
    catchment_area_m2,
    runoff_coefficient,
    tank_capacity_liters,
    initial_storage_liters=0
):
    """
    Simulate tank levels based on forecasted rainfall and optimized usage.
    
    Parameters:
        merged_df (pd.DataFrame): Must have columns ['date', 'predicted_rainfall_mm', 'optimized_usage_liters']
        catchment_area_m2 (float): Catchment area in square meters
        runoff_coefficient (float): Runoff coefficient (0.0 to 1.0)
        tank_capacity_liters (float): Tank capacity in liters
        initial_storage_liters (float): Initial storage level in liters
        
    Returns:
        pd.DataFrame: Simulation results with columns:
            ['date', 'rainfall_mm', 'inflow_liters', 'usage_liters', 
             'storage_liters', 'overflow_liters', 'shortage_liters']
    """
    results = []
    current_storage = initial_storage_liters

    for _, row in merged_df.iterrows():
        date = row['date']
        rainfall_mm = row['predicted_rainfall_mm']
        daily_usage_liters = row['optimized_usage_liters']

        inflow_liters = rainfall_mm * catchment_area_m2 * runoff_coefficient
        current_storage += inflow_liters

        overflow = 0
        if current_storage > tank_capacity_liters:
            overflow = current_storage - tank_capacity_liters
            current_storage = tank_capacity_liters

        shortage = 0
        if current_storage >= daily_usage_liters:
            current_storage -= daily_usage_liters
        else:
            shortage = daily_usage_liters - current_storage
            current_storage = 0

        results.append({
            "date": date,
            "rainfall_mm": rainfall_mm,
            "inflow_liters": round(inflow_liters, 2),
            "usage_liters": round(daily_usage_liters, 2),
            "storage_liters": round(current_storage, 2),
            "overflow_liters": round(overflow, 2),
            "shortage_liters": round(shortage, 2)
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Standalone run for testing
    import sys
    
    if len(sys.argv) != 5:
        print("Usage: python tank_simulation.py <catchment_area_m2> <runoff_coefficient> <tank_capacity_liters> <initial_storage_liters>")
        sys.exit(1)
        
    catchment_area_m2 = float(sys.argv[1])
    runoff_coefficient = float(sys.argv[2])
    tank_capacity_liters = float(sys.argv[3])
    initial_storage_liters = float(sys.argv[4])

    # For standalone testing, read from CSV
    try:
        forecast_df = pd.read_csv("outputs/final_plan.csv", parse_dates=["date"])
        
        simulated_df = simulate_tank_levels(
            merged_df=forecast_df,
            catchment_area_m2=catchment_area_m2,
            runoff_coefficient=runoff_coefficient,
            tank_capacity_liters=tank_capacity_liters,
            initial_storage_liters=initial_storage_liters
        )

        simulated_df.to_csv("outputs/tank_simulation_next_7_days.csv", index=False)
        print("✅ Tank simulation saved to outputs/tank_simulation_next_7_days.csv")
        print(simulated_df)
        
    except FileNotFoundError:
        print("❌ Error: outputs/final_plan.csv not found. Run the full pipeline first.")
        print("Or use the function directly by importing it and passing a DataFrame.")
