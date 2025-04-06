import json
import json
import os
import math
from collections import defaultdict
import statistics # Use Python's built-in statistics module
import warnings

# Suppress RuntimeWarning for mean of empty slice, etc.
warnings.filterwarnings("ignore", category=RuntimeWarning)

def calculate_positional_stats(input_db_path='backend/database.json', output_path='backend/average_statistics_by_position.json'):
    """
    Calculates average and standard deviation for player stats grouped by position.

    Args:
        input_db_path (str): Path to the input player database JSON file.
        output_path (str): Path to save the calculated statistics JSON file.
    """
    print(f"Loading player database from: {input_db_path}")
    try:
        # Try different paths relative to the script location or project root
        script_dir = os.path.dirname(__file__)
        paths_to_try = [
            input_db_path,
            os.path.join(script_dir, input_db_path),
            os.path.join(script_dir, '..', input_db_path) # If script is in a subdir like 'scripts'
        ]
        
        db_file = None
        for path in paths_to_try:
            if os.path.exists(path):
                db_file = path
                break
        
        if not db_file:
             raise FileNotFoundError(f"Could not find {input_db_path} in checked locations.")

        with open(db_file, 'r', encoding='utf-8') as f:
            database = json.load(f)
        print(f"Successfully loaded database with {len(database)} players from {db_file}.")

    except FileNotFoundError:
        print(f"Error: Input database file not found at {input_db_path} or related paths.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_db_path}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during loading: {e}")
        return

    positional_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    all_metrics = set() # Keep track of all unique metrics encountered (category, metric_name)

    print("Grouping players by primary position and collecting stats...")
    players_processed = 0
    players_skipped_no_pos = 0
    players_skipped_invalid_data = 0

    # Group players by primary position and collect stats
    for player_name, player_data in database.items():
        if not isinstance(player_data, dict):
            # print(f"Skipping invalid player data for {player_name}")
            players_skipped_invalid_data += 1
            continue

        primary_position = None
        positions = player_data.get("positions")
        if isinstance(positions, list) and len(positions) > 0:
            # Assuming the first position listed is the primary one
            first_pos_info = positions[0]
            if isinstance(first_pos_info, dict) and "position" in first_pos_info:
                pos_details = first_pos_info["position"]
                if isinstance(pos_details, dict) and "code" in pos_details:
                    primary_position = pos_details["code"]

        if not primary_position:
            # print(f"Skipping player {player_name} due to missing primary position.")
            players_skipped_no_pos += 1
            continue

        players_processed += 1
        # Collect stats from 'total', 'average', 'percent' keys
        for category in ["total", "average", "percent"]:
            stats_category = player_data.get(category)
            if isinstance(stats_category, dict):
                for metric, value in stats_category.items():
                    # Ensure value is numeric (int or float) and not NaN
                    if isinstance(value, (int, float)) and not math.isnan(value):
                        positional_data[primary_position][category][metric].append(value)
                        all_metrics.add((category, metric))
                    # else:
                        # print(f"Skipping non-numeric/NaN value for {player_name}, {category}.{metric}: {value}")

    print(f"Processed {players_processed} players.")
    if players_skipped_no_pos > 0:
        print(f"Skipped {players_skipped_no_pos} players due to missing primary position.")
    if players_skipped_invalid_data > 0:
         print(f"Skipped {players_skipped_invalid_data} players due to invalid data format.")
    print(f"Found {len(positional_data)} unique primary positions.")
    print(f"Found {len(all_metrics)} unique metrics across all categories.")
    print("Calculating average and standard deviation for each metric...")

    calculated_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # Calculate stats
    for position, categories in positional_data.items():
        # print(f"  Processing position: {position}")
        for category, metrics in categories.items():
            for metric, values in metrics.items():
                avg = 0.0
                std_dev = 0.0
                if values: # Ensure there are values to calculate
                    try:
                        # Calculate mean using statistics.mean
                        avg = float(statistics.mean(values))
                        # Calculate population standard deviation using statistics.pstdev
                        # Requires at least one data point
                        if len(values) > 0:
                           std_dev = float(statistics.pstdev(values))
                        # Handle cases with only one data point (std dev is 0)
                        else:
                           std_dev = 0.0
                    except statistics.StatisticsError:
                        # Handle potential errors if list is empty after filtering (should not happen here)
                        avg = 0.0
                        std_dev = 0.0
                    except Exception as e:
                         print(f"Unexpected error calculating stats for {position}.{category}.{metric}: {e}")
                         avg = 0.0
                         std_dev = 0.0

                calculated_stats[position][category][metric] = {'average': avg, 'std': std_dev}

    # Ensure all positions have entries for all metrics found across the dataset
    print("Ensuring all positions have entries for all metrics...")
    all_positions = list(calculated_stats.keys())
    metrics_added_count = 0
    for position in all_positions:
        for category, metric in all_metrics:
            if metric not in calculated_stats[position][category]:
                 calculated_stats[position][category][metric] = {'average': 0.0, 'std': 0.0}
                 metrics_added_count += 1
                 # print(f"    Added default entry for missing metric: {position}.{category}.{metric}")
    if metrics_added_count > 0:
        print(f"Added {metrics_added_count} default entries for missing metrics across positions.")


    print(f"Saving calculated stats to: {output_path}")
    try:
        # Ensure the directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
             os.makedirs(output_dir)
             print(f"Created directory: {output_dir}")

        with open(output_path, 'w', encoding='utf-8') as f:
            # Convert defaultdicts to regular dicts for clean JSON output
            final_output = json.loads(json.dumps(calculated_stats))
            json.dump(final_output, f, ensure_ascii=False, indent=4)
        print(f"Successfully saved statistics to {output_path}.")
    except IOError as e:
        print(f"Error saving statistics file: {e}")
    except Exception as e:
         print(f"An unexpected error occurred during saving: {e}")

if __name__ == "__main__":
    # Allow overriding paths via environment variables if needed, otherwise use defaults
    # Default paths assume the script is run from the project root (KatenaScout-1)
    db_path = os.environ.get('KATENA_DB_PATH', 'backend/database.json')
    output_stats_path = os.environ.get('KATENA_AVG_STATS_PATH', 'backend/average_statistics_by_position.json')
    
    print(f"Using database path: {db_path}")
    print(f"Using output path: {output_stats_path}")
    
    calculate_positional_stats(input_db_path=db_path, output_path=output_stats_path)
