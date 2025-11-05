import pandas as pd
import numpy as np
import random
from src.fitness_function import fitness_function
import os

def run_ga_optimization(
    forecast_df,
    catchment_area_m2=100,
    runoff_coefficient=0.85,
    tank_capacity_liters=3000,
    initial_storage_liters=1500,
    usage_min=300,
    usage_max=800,
    population_size=50,
    generations=100,
    mutation_rate=0.1
):
    """
    Run Genetic Algorithm optimization on forecasted rainfall data.

    Parameters:
        forecast_df (pd.DataFrame): Must have columns ['date', 'predicted_rainfall_mm']
        catchment_area_m2, runoff_coefficient, tank_capacity_liters, initial_storage_liters: tank parameters
        usage_min, usage_max: daily usage constraints in liters
        population_size, generations, mutation_rate: GA settings

    Returns:
        tuple: (optimized_usage_df, merged_df)
    """

    # Ensure output directory
    os.makedirs("outputs", exist_ok=True)

    def create_individual():
        """Random usage plan for 7 days."""
        return [random.uniform(usage_min, usage_max) for _ in range(len(forecast_df))]

    def mutate(individual):
        """Randomly tweak a day's usage."""
        day = random.randint(0, len(individual)-1)
        individual[day] = random.uniform(usage_min, usage_max)
        return individual

    def crossover(parent1, parent2):
        """Single point crossover."""
        point = random.randint(1, len(parent1)-1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    # Initialize population
    population = [create_individual() for _ in range(population_size)]

    for gen in range(generations):
        # Evaluate fitness
        scores = [
            (
                fitness_function(
                    ind, forecast_df,
                    catchment_area_m2, runoff_coefficient,
                    tank_capacity_liters, initial_storage_liters
                ),
                ind
            )
            for ind in population
        ]
        scores.sort(reverse=True, key=lambda x: x[0])
        best_score, best_individual = scores[0]

        if gen % 10 == 0:
            print(f"Generation {gen}: Best Score = {best_score:.2f}")

        # Selection (top 50%)
        selected = [ind for _, ind in scores[:population_size // 2]]

        # Crossover & Mutation
        children = []
        while len(children) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child1, child2 = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)
            children.extend([child1, child2])

        population = children

    # Final best plan
    final_score, final_plan = scores[0]
    print("\n✅ Optimization complete")
    print(f"Best Score: {final_score:.2f}")
    print("Best Plan (liters/day):", [round(x, 2) for x in final_plan])

    # Save optimized plan
    optimized_df = pd.DataFrame({
        "date": forecast_df["date"],
        "usage_liters": [round(x, 2) for x in final_plan]
    })
    optimized_df.to_csv("outputs/optimized_plan.csv", index=False)

    # Merge with forecast
    merged_df = forecast_df.copy()
    merged_df["optimized_usage_liters"] = optimized_df["usage_liters"]
    merged_df.to_csv("outputs/final_plan.csv", index=False)

    return optimized_df, merged_df


if __name__ == "__main__":
    # Standalone run
    forecast_df = pd.read_csv("outputs/predictions_next_7_days_on_NASA_data.csv", parse_dates=["date"])
    run_ga_optimization(forecast_df)
