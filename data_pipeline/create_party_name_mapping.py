import csv

input = "./data_pipeline/processed_csv/party_data/2024_party_code_candidates.csv"
map_set = set()

with open(input, mode='r') as file:
    reader = csv.DictReader(file)

    for row in reader:
        map_set.add((row['party_name'], row['party_code']))

for map in map_set:
    print(f'"{map[1]}":"{map[0]}",')