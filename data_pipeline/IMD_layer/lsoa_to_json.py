import pandas as pd
import json


#NEEDS REFACTORING BIGTIME 



# Load the dataset
data = pd.read_csv("/home/sid/Desktop/geo_project/data_pipeline/test.csv")  # Replace with your actual file path

print(data.columns[0])
# Ensure the dataset columns are named properly
new_columns = [
    "lsoa11_id", "local_authority_name", "absolute_deprivation_ranking", "relative_deprivation_ranking_pct", 
    "deprivation_decile", "local_authority_rank", "local_authority_rank_pct", "local_authority_decile", "lsoa11cd_id", "lad22nm", "lsoa21cd", "lsoa21nm", "wd24cd", "wd24nm"
]


# for i in range(len(data.columns)):
#     print(f"dataframe index {i}= ", data.columns[i], f" | new col index {i}= ", new_columns[i])

# Create a dictionary to store the nested structure
output = {}

placeholder = ""
rel_vals = []
# Loop through the rows to create the nested structure
for idx, row in data.iterrows():

    # Check if the wd24cd (e.g., 'E05010950') already exists in the dictionary
    wd24cd = row['wd24cd']
    
    if wd24cd not in output:
        output[wd24cd] = {
            "lsoa21nm": row['lsoa21nm'], #data health check to ensure all fir within ward!
            "lsoa_number_of": len(data[data['wd24cd'] == wd24cd]),  # Count of LSOAs for the region
            # "wd24nm": row['wd24nm'],
            "local_authority_rank_pct": row['local_authority_rank_pct'],  # Assuming code_43 is the local authority rank percentage
            "lsoa11_ids": []  # Initialize an empty list to store LSOA details

        }
    
    # Append LSOA details to the list under 'lsoa11_ids'
    output[wd24cd]['lsoa11_ids'].append({
        "lsoa11_id": idx,
        "absolute_deprivation_ranking": row['local_authority_name'], #need to find where displacement happens! this is workaround
        "relative_deprivation_ranking_pct": row['absolute_deprivation_ranking'],
        "deprivation_decile": row['relative_deprivation_ranking_pct']
    })

# Convert the dictionary to a JSON string
json_output = json.dumps(output, indent=2)

# Save to a file
with open("/home/sid/Desktop/geo_project/data_pipeline/output.json", "w") as f:
    f.write(json_output)

print("JSON output saved to output.json")
