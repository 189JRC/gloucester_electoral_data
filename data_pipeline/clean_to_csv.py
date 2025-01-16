from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
import json

# standard spark session stuff
#-------------------------------------------------
spark = SparkSession.builder.getOrCreate()


spark = (SparkSession.builder
                     .appName("Counting word occurences from a book.")
                     .getOrCreate())
#./data_pipeline/preprocessed/2024_elections_results_by_candidate_uk_parliament.csv

##################################################
# PARTY DATA
##################################################
# processing steps
#-------------------------------------------------

def make_party_dataset_csv(fname):

    # read from file.
    # this process should be replicable across different like datasets
    #-------------------------------------------------

    #e.g. "./data_pipeline/preprocessed/2024_elections_results_by_candidate_uk_parliament.csv"
    input_file = "./data_pipeline/preprocessed/" + fname 
    df = spark.read.csv(input_file, inferSchema=True, header=True)


    # sanity check
    #-------------------------------------------------
    #4515 - total number of candidates (ergo rows)
    df.count() 

    # firstly, format column names to snake case
    df = df.toDF(*[c.lower().replace(" ", "_") for c in df.columns])

    # secondly, make a party data reference table
    party_data = df.select(
        F.col('main_party_name').alias('party_name'), 
        F.col('main_party_abbreviation').alias('party_code'), 
        F.col('main_party_mnis_id').alias('party_id'),
        F.col('main_party_url').alias('url'),
        F.col('candidate_vote_share').alias('vote_share'),
        F.col('candidate_vote_count').alias('vote_count')
                        )

    # all nulls are independents. these nulls are lost in groupBy 
    # party.count() is 97 and not 98 -> need to rename entry to keep it
    # format entries to snake case for both columns
    party_data_with_independents = party_data.withColumn(
        "party_name",
        F.when(F.col("party_name").isNull(), "Independent").otherwise(F.col("party_name"))
        ).withColumn(
            "party_code",
            F.when(F.col("party_code").isNull(), "Independent").otherwise(F.col("party_code"))
            ).withColumn( 
            "party_name",
            F.when(F.col("party_name").isNotNull(),
                F.regexp_replace(F.lower(F.col("party_name")), " ", "_")
                ).otherwise(F.col("party_name"))
                ).withColumn(
                "party_code",
                F.when(F.col("party_code").isNotNull(),
                    F.regexp_replace(F.lower(F.col("party_code")), " ", "_")
                    ).otherwise(F.col("party_code"))
                        )

    grouped_candidates = party_data_with_independents.groupBy(["party_name"]).count()

    # Group by party_name and sum the vote_count
    party_vote_summary = party_data_with_independents.groupBy("party_name").agg(
        F.sum("vote_count").alias("total_vote_count")
    )
    ###
    joined_party_data = party_data_with_independents.join(grouped_candidates, on="party_name")
    joined_party_data = joined_party_data.distinct()

    joined_party_data = joined_party_data.join(party_vote_summary, on="party_name")

    joined_party_data = joined_party_data.orderBy(F.col('party_name').asc())
    joined_party_data = joined_party_data.withColumnRenamed("count", "candidates_ran")

    output_path = "./data_pipeline/processed/2024_party_name_code_id_candidates_ran.csv"

    joined_party_data.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

    return True

fname = input("enter filename (must be in processed/): ")
make_party_dataset_csv(fname)

##################################################
# CANDINDATE DATA
##################################################

###V#START###########
input = "./data_pipeline/preprocessed/2024_elections_results_by_candidate_uk_parliament.csv"

df = spark.read.csv(input, inferSchema=True, header=True)

columns_wanted= ['Country name', 'English region name','English region geographic code','Constituency name',
 'Constituency geographic code', 'Constituency designation', 'Electorate', 'Election valid vote count',
 'Election invalid vote count', 'Election result summary', 'Candidate family name', 'Candidate given name',
 'Candidate MNIS ID', 'Candidate is sitting MP', 'Candidate is former MP', 'Main party abbreviation',
 'Candidate is standing as independent', 'Candidate vote count','Candidate vote share', 'Candidate vote change',
 'Majority',
 'Candidate result position'
 ]

df = df.select(*[F.col(c) for c in columns_wanted])
df = df.toDF(*[c.lower().replace(" ", "_") for c in df.columns])
df = df.withColumn("full_name", F.concat(F.col("candidate_given_name"), F.lit(" "), F.col("candidate_family_name")))
df = df.drop(*['candidate_given_name', 'candidate_family_name'])

df.columns


snaked_columns = ['english_region_name', 'english_region_geographic_code', 'constituency_name', 'constituency_geographic_code', 'constituency_designation', 'electorate', 'election_valid_vote_count', 'election_invalid_vote_count', 'election_result_summary', 'candidate_family_name', 'candidate_given_name', 'candidate_mnis_id', 'candidate_is_sitting_mp', 'candidate_is_former_mp', 'main_party_abbreviation', 'candidate_is_standing_as_independent', 'candidate_vote_count', 'candidate_vote_share', 'candidate_vote_change', 'majority', 'candidate_result_position']
tupes = []

for column in snaked_columns:
  tupes.append((column, None))


column_mapping = [('english_region_name', "region_en"), 
('english_region_geographic_code', 'en_geo_code'), 
('constituency_name', 'constituency_name'), 
('constituency_geographic_code', 'const_geo_code'), 
('constituency_designation', 'const_designation'), 
('electorate', 'electorate'), 
('election_valid_vote_count', 'vote_count'), 
('election_invalid_vote_count', 'inv_vote_count'), 
('election_result_summary', 'result_summary'), 
('candidate_family_name', 'candidate_name'), 
('candidate_mnis_id', 'candidate_id'), 
('candidate_is_sitting_mp', 'sitting_mp'), 
('candidate_is_former_mp', 'former_mp'), 
('main_party_abbreviation', 'party'), 
('candidate_is_standing_as_independent', 'indy_candidate'), 
('candidate_vote_count', 'c_vote_count'), 
('candidate_vote_share', 'c_vote_share'), 
('candidate_vote_change', 'c_vote_change'), 
('majority', 'majority'), 
('candidate_result_position', 'rank')]


for old, new in column_mapping:
  df = df.withColumnRenamed(old, new)

df_updated = df.withColumn("region_en", F.when(F.col("country_name") != "England", F.col("country_name")).otherwise(F.col("region_en")))
df_updated = df_updated.drop(F.col('country_name')).drop(F.col('en_geo_code'))
df = df_updated.withColumn(
    "party",
    F.when(F.col("indy_candidate") == False, F.col("party")).otherwise(F.lit("Indy"))
)
df = df.drop(F.col('indy_candidate'))
df = df.withColumnRenamed("region_en", "region")

output_path = "./data_pipeline/processed_csv/candidate_data/2024_candidates.csv"

df.coalesce(1).write.csv(output_path, header=True, mode="overwrite")