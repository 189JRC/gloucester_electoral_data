import json

# Load JSON from the file
with open('/home/sid/Desktop/geo_project/data_pipeline/deprivation.json', 'r') as file:
    data = json.load(file)  # This loads the JSON into a Python dictionary

# Your wards data
wards_data = {
    "Abbeydale": 74.25,
    "Abbeymead": 82.6666666666667,
    "Barnwood": 78.6666666666667,
    "Barton and Tredworth": 16.2857142857143,
    "Coney Hill": 18.6666666666667,
    "Elmbridge": 73.0,
    "Grange": 56.75,
    "Hucclecote": 80.0,
    "Kingsholm and Wotton": 28.75,
    "Kingsway": 56.0,
    "Longlevens": 86.8333333333333,
    "Matson, Robinswood and White City": 18.5714285714286,
    "Moreland": 29.4285714285714,
    "Podsmead": 24.5,
    "Quedgeley Fieldcourt": 62.0,
    "Quedgeley Severn Vale": 81.25,
    "Tuffley": 43.5,
    "Westgate": 21.0
}

# Function to add mean absolute deprivation ranking to each ward's data
def add_mean_ranking_to_data(data, wards_data):
    for ward, ward_data in data.items():
        # If the ward is in wards_data, add the mean ranking
        if ward in wards_data:
            ward_data['mean_absolute_deprivation_ranking'] = wards_data[ward]
    
    return data

# Add the mean ranking to the original data
updated_data = add_mean_ranking_to_data(data, wards_data)

# Save the updated data back to a file
with open('/home/sid/Desktop/geo_project/data_pipeline/deprivation_updated.json', 'w') as file:
    json.dump(updated_data, file, indent=2)

# Print the updated data
print(json.dumps(updated_data, indent=2))
