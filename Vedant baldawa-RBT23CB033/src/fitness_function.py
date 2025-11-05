import numpy as np

def fitness_function(usage_plan, forecast_df, catchment_area_m2, runoff_coefficient, tank_capacity_liters, initial_storage_liters):
    """
    Calculate the fitness score for a 7-day usage plan.

    usage_plan: list of daily usage in liters (length = 7)
    """
    storage = initial_storage_liters
    overflow_penalty = 0
    shortage_penalty = 0

    for day, usage in enumerate(usage_plan):
        # Rainwater collected
        rainfall_mm = forecast_df.iloc[day]["predicted_rainfall_mm"]
        inflow_liters = rainfall_mm * catchment_area_m2 * runoff_coefficient

        # Update storage
        storage += inflow_liters
        storage -= usage

        # Penalties
        if storage > tank_capacity_liters:
            overflow_penalty += (storage - tank_capacity_liters) * 2
            storage = tank_capacity_liters

        if storage < 0:
            shortage_penalty += abs(storage) * 5
            storage = 0

    # Base score
    score = 1000 - (overflow_penalty + shortage_penalty)
    return score
