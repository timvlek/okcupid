import numpy as np
import pandas as pd
import scipy.stats
from typing import Any

def main():
    """
    Main function to create a DataFrame with test data and test function operation.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with test data
    """
    # Set random.seed for reproducibility
    np.random.seed(0)

    # Create a DataFrame with test data
    data = pd.DataFrame({
        "Integer": np.random.randint(100, 200, 100),
        "Float": np.random.random(100),
        "Boolean": np.random.choice([True, False], 100),
        "Category": np.random.choice(["A", "B", "C"], 100),
        "Datetime": pd.date_range(start="1/1/2020", periods=100),
        "Timedelta": [pd.Timedelta(days=i) for i in range(100)],
        "Text": np.random.choice(["foo", "bar", "baz"], 100),
        "Object": [f"object_{i}" for i in range(100)]
    })

    # Calculate the results from normal_tests
    normal_results = normal_tests(data)

    # Calculate the results gof_tests
    gof_results = gof_tests(data)

    # # Return results
    return normal_results, gof_results

# Run the main function if the script is executed
if __name__ == "__main__":
    main()