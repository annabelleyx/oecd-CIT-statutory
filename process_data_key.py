"""
The below code produces the corresponding keys for data categories in the OECD dataset on corporate income tax statutory 
and targeted small business rates for all OECD countries between 2000-2024.

"""

import json
import pandas as pd

# Load the JSON data
with open('oecd_data.json', 'r') as file:
    data = json.load(file)

# Function to extract dimension details
def extract_dimension_details(dimension):
    return {value['id']: value['name'] for value in dimension['values']}

# Extract dimension details
dimensions = data['data']['structure']['dimensions']['series']
dimension_details = {dim['id']: extract_dimension_details(dim) for dim in dimensions}

# Add observation dimension (usually Year)
observation_dimension = data['data']['structure']['dimensions']['observation'][0]
dimension_details[observation_dimension['id']] = extract_dimension_details(observation_dimension)

# Create a DataFrame for each dimension
dataframes = []
for dim_id, dim_values in dimension_details.items():
    df = pd.DataFrame(list(dim_values.items()), columns=['Code', 'Description'])
    df['Dimension'] = dim_id
    dataframes.append(df)

# Combine all DataFrames
key_df = pd.concat(dataframes, ignore_index=True)

# Sort the DataFrame
key_df = key_df.sort_values(['Dimension', 'Code'])

# Reorder columns
key_df = key_df[['Dimension', 'Code', 'Description']]

# Print the first few rows of the key
print("\nFirst few rows of the key:")
print(key_df.head(10))

# Save the key to an Excel file
key_df.to_excel('oecd_tax_rates_key.xlsx', index=False)

print("Data key has been successfully created and saved to 'oecd_tax_rates_key.xlsx'.")

# Print unique values for each dimension
for dimension in key_df['Dimension'].unique():
    print(f"\nUnique values for {dimension}:")
    subset = key_df[key_df['Dimension'] == dimension]
    for _, row in subset.iterrows():
        print(f"  {row['Code']}: {row['Description']}")