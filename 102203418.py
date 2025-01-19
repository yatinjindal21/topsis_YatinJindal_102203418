import sys
import pandas as pd
import numpy as np

def topsis(input_file, weights, impacts, output_file):
    # Read the input file
    data = pd.read_csv(input_file)
    
    # Validate input data
    if len(data.columns) < 3:
        raise ValueError("Input file must have at least three columns.")
    
    if len(weights) != len(data.columns) - 1:
        raise ValueError("Number of weights must match the number of criteria.")
    
    if len(impacts) != len(data.columns) - 1:
        raise ValueError("Number of impacts must match the number of criteria.")
    
    if not all(impact in ["+", "-"] for impact in impacts):
        raise ValueError("Impacts must be either '+' or '-'.")

    # Extract decision matrix and normalize
    matrix = data.iloc[:, 1:].values
    norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    # Apply weights
    weighted_matrix = norm_matrix * weights

    # Calculate ideal best and worst
    ideal_best = np.where(np.array(impacts) == "+", weighted_matrix.max(axis=0), weighted_matrix.min(axis=0))
    ideal_worst = np.where(np.array(impacts) == "+", weighted_matrix.min(axis=0), weighted_matrix.max(axis=0))

    # Calculate Euclidean distances
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # Calculate TOPSIS scores
    scores = dist_worst / (dist_best + dist_worst)
    ranks = scores.argsort()[::-1] + 1

    # Append scores and ranks to the input data
    data["Topsis Score"] = scores
    data["Rank"] = ranks

    # Save output file
    data.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

# Command-line execution
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <RollNumber>.py <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    weights = list(map(float, sys.argv[2].split(",")))
    impacts = sys.argv[3].split(",")
    output_file = sys.argv[4]
    
    try:
        topsis(input_file, weights, impacts, output_file)
    except Exception as e:
        print(e)
        sys.exit(1)
