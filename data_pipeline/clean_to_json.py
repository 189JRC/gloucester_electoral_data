# we are aiming for 
# ons_id {
#     region_name,
#     results: [
#         1: [
#             name etc.
#         ]
#     ]
# }

import csv
import json

# Initialize an empty dictionary to store data
full_candidate_dict_geo_code_keys = {}
const_geo_code = -9999
# Open and read the CSV file
input = "./data_pipeline/processed_csv/candidate_data/2024_candidates.csv"


def read_csv_write_json(input):
    with open(input, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:

            #check if this is a new block
            #if it is make new geo_dict, (with candidate list with 1 entry)
            #if not append to candidate list for that geo code
            if row['const_geo_code'] != const_geo_code:
                new_section = True
                const_geo_code = row['const_geo_code']
                votes_to_win = 0
                majority_as_pct_votes = ( int(row['majority']) / int(int(row['vote_count'])) ) * 100
                winning_vote_count = int(row['c_vote_count']) # needed to estimate rank 2+ candidates' chances
            else:
                new_section = False
                votes_to_win = winning_vote_count - int(row['c_vote_count'])

            if new_section == True:
                #make the dict and enter it into candidate_dict 
                full_candidate_dict_geo_code_keys[const_geo_code] = {
                    "constituency_name": row['constituency_name'],
                    "region": row['region'],
                    "winning_party": row['party'],
                    "const_designation": row['const_designation'],
                    "electorate": int(row['electorate']),
                    "votes_counted": int(row['vote_count']),
                    "inv_votes_counted": int(row['inv_vote_count']),
                    "result_summary": row['result_summary'],
                    "majority": int(row['majority']),
                    "majority_pct_votes": majority_as_pct_votes,
                    "candidates": [{
                        "rank": int(row['rank']),
                        "candidate_id": int(row['candidate_id']) if row['candidate_id'] else None,
                        "full_name": row['full_name'],
                        "sitting_mp" : row['sitting_mp'],
                        "former_mp": row['former_mp'],
                        "party": row['party'],
                        "vote_count": int(row['c_vote_count']),
                        "vote_share": float(row['c_vote_share']),
                        "vote_change": float(row['c_vote_change']) if row['c_vote_change'] else None,
                        "votes_to_win": 0
                        }]
                    }

            if new_section == False:
                #if not new block append to candidate list for that geo code
                new_candidate_entry = {
                    "rank": int(row['rank']),
                    "candidate_id": int(row['candidate_id']) if row['candidate_id'] else None,
                    "full_name": row['full_name'],
                    "sitting_mp" : row['sitting_mp'],
                    "former_mp": row['former_mp'],
                    "party": row['party'],
                    "vote_count": int(row['c_vote_count']),
                    "vote_share": float(row['c_vote_share']),
                    "vote_change": float(row['c_vote_change']) if row['c_vote_change'] else None,
                    "votes_to_win": votes_to_win
                    }
                
                full_candidate_dict_geo_code_keys[row['const_geo_code']]['candidates'].append(new_candidate_entry)
            

    import os 
    output = os.path.abspath("./data_pipeline/processed_json/candidate_data/2024_candidates.json")

    # Convert the dictionary to a JSON string
    json_data = json.dumps(full_candidate_dict_geo_code_keys, indent=4)

    with open(output, 'w') as json_file:
        json_file.write(json_data)

    print("printed to:", output) 


