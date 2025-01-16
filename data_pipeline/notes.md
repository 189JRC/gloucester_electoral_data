1.20241224
2024 results with electorate size - https://electionresults.parliament.uk/general-elections/6/constituency-areas

2.20250111
the front end data sources should be sim linked to the data pipeline
I have started with 2024_candidates.json
This will be NEED TO BE SCRIPTED in any automated deployment
# Create a symlink
ln -s /path/to/original /path/to/symlink
ln -s /home/sid/Desktop/geo_project/data_pipeline/processed_json/candidate_data/2024_candidates.json /home/sid/Desktop/geo_project/frontend/public/2024_candidates_symlink