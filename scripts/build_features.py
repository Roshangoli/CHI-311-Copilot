
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

    

    print(f"Saving feature-engineered data to {output_path}")
    # df.to_csv(output_path, index=False)
    print("Feature engineering script stub executed. R1 to implement logic.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build features for 311 data.")
    parser.add_argument("--input", type=str, default="data/raw/311_service_requests.csv", help="Input raw CSV file path.")
    parser.add_argument("--output", type=str, default="data/processed/features.csv", help="Output feature CSV file path.")
    args = parser.parse_args()

    

    build_features(args.input, args.output)
