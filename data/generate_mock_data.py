import pandas as pd
import numpy as np
from pathlib import Path
import argparse

# Generates mock data for A/B Testing scenario
def generate_ab_test_data(n_users=10000, seed=42):

    np.random.seed(seed)
    
    # 1. Generates user IDs
    user_ids = np.arange(1, n_users + 1)
    
    # 2. Attributes half users to group A and half users to group B
    groups = np.random.choice(['A', 'B'], size=n_users, p=[0.5, 0.5])
    
    # 3. Defines conversion rates (B is slightly better than A)
    conversion_rate_A = 0.10  # 10% de conversão
    conversion_rate_B = 0.12  # 12% de conversão
    
    # 4. Generates conversions and revenues
    conversions = []
    revenues = []

    # For each group generates 1 (converted) or 0 (didn't convert) with given conversion rate.
    # If converted, generates a revenue
    for group in groups:
        if group == 'A':
            converted = np.random.binomial(1, conversion_rate_A)
            revenue = np.random.normal(50, 10) if converted else 0.0
        else:
            # Generates again for group B
            converted = np.random.binomial(1, conversion_rate_B)
            revenue = np.random.normal(55, 10) if converted else 0.0
            
        conversions.append(converted)
        
        # Makes sure the revenue is non-negative
        revenues.append(max(0, revenue))
        
    # 5. Creates and returns a data frame
    df = pd.DataFrame({
        'user_id': user_ids,
        'group': groups,
        'converted': conversions,
        'revenue': revenues
    })
    
    return df

def main():

    # Parse the arguments from the command line to extract the desired number of samples.
    # The default value is 5000
    parser = argparse.ArgumentParser(description="Generates mock data for A/B testing")
    parser.add_argument("--n_samples", type=int, help="The number of samples", default=5000)
    args = parser.parse_args()

    # Generates the data and saves to the data folder
    script_dir = Path(__file__).parent.absolute()
    mock_data = generate_ab_test_data(n_users=args.n_samples)
    mock_data.to_csv(f'{script_dir}/ab_test_data.csv', index=False)

if __name__ == '__main__':
    main()