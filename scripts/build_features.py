
# scripts/build_features.py
import argparse
import pandas as pd

def build_features(input_path: str, output_path: str):
    """
    Loads raw data, engineers features, and saves the result.
    This script is designed to prevent data leakage by ensuring features
    are generated based on a snapshot in time.

    Args:
        input_path: Path to the raw data CSV file.
        output_path: Path to save the feature-engineered data CSV.
    """
    print(f"Loading raw data from {input_path}")
    df = pd.read_csv(input_path)

    # TODO: R1 to convert date columns to datetime objects
    # df['created_date'] = pd.to_datetime(df['created_date'])
    # df['closed_date'] = pd.to_datetime(df['closed_date'])

    # TODO: R1 to calculate the target variable 'days_to_close' for completed requests
    # df['days_to_close'] = (df['closed_date'] - df['created_date']).dt.days

    # --- Leakage-Safe Feature Engineering ---
    # All features should be based on information available at `created_date`.

    # TODO: R1 to implement backlog features.
    # Example: count of open requests in the same ward/category in the last 7/30 days.
    # This requires a time-aware calculation, iterating through sorted data.

    # TODO: R1 to implement rolling median resolution times.
    # Example: median 'days_to_close' for the same ward/category in the last 30/90 days.

    # TODO: R1 to implement seasonality features.
    # df['day_of_week'] = df['created_date'].dt.dayofweek
    # df['month'] = df['created_date'].dt.month
    # df['is_holiday'] = ... # (requires a holiday calendar)

    # TODO: R1 to add categorical and spatial features.
    # df['ward'] = df['ward'].astype('category')
    # df['community_area'] = df['community_area'].astype('category')
    # df['category'] = df['sr_type'].astype('category')

    print(f"Saving feature-engineered data to {output_path}")
    # df.to_csv(output_path, index=False)
    print("Feature engineering script stub executed. R1 to implement logic.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build features for 311 data.")
    parser.add_argument("--input", type=str, default="data/raw/311_service_requests.csv", help="Input raw CSV file path.")
    parser.add_argument("--output", type=str, default="data/processed/features.csv", help="Output feature CSV file path.")
    args = parser.parse_args()

    # In a real script, you would ensure the output directory exists
    # import os
    # os.makedirs(os.path.dirname(args.output), exist_ok=True)

    build_features(args.input, args.output)
