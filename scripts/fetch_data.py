
# scripts/fetch_data.py
import os
import argparse
from datetime import datetime, timedelta
import pandas as pd
import requests

# TODO: R1 to confirm dataset ID and category names from Chicago Data Portal
DATASET_ID = "f294-26ae"  # 311 Service Requests
CATEGORIES = ["Pothole in Street", "Street Lights - All/Out", "Sanitation Code Violation"]
APP_TOKEN = os.environ.get("CHICAGO_DATA_APP_TOKEN") # It'''s good practice to use an app token

def fetch_data(months_to_fetch: int, categories: list[str], output_path: str):
    """
    Fetches 311 service request data from the Chicago Open Data Portal API.

    Args:
        months_to_fetch: Number of past months of data to retrieve.
        categories: A list of service request types to fetch.
        output_path: The file path to save the combined CSV.
    """
    if not APP_TOKEN:
        print("Warning: CHICAGO_DATA_APP_TOKEN environment variable not set. API requests may be throttled.")

    client = requests.Session()
    base_url = f"https://data.cityofchicago.org/resource/{DATASET_ID}.json"

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months_to_fetch * 30)
    soql_where_clause = f"created_date >= ''{start_date.isoformat()}'' and sr_type in ({", ".join([f"''{cat}''" for cat in categories])})"

    # TODO: R1 to implement robust pagination if record count exceeds API limits (e.g., 50,000)
    params = {
        "$where": soql_where_clause,
        "$limit": 50000, # Default Socrata limit, may need pagination
        "$$app_token": APP_TOKEN
    }

    print(f"Fetching data for categories: {categories} from {start_date.date()} to {end_date.date()}")

    try:
        response = client.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            print("No data returned from API.")
            return

        df = pd.DataFrame(data)
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Successfully downloaded {len(df)} records to {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Chicago 311 data.")
    parser.add_argument("--months", type=int, default=24, help="Number of past months to fetch.")
    # Changed default to reflect a more realistic structure
    parser.add_argument("--output", type=str, default="data/raw/311_service_requests.csv", help="Output CSV file path.")
    args = parser.parse_args()

    fetch_data(args.months, CATEGORIES, args.output)
