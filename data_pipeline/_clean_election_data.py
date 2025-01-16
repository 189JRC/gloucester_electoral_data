#cleans elections csv
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
import json

spark = SparkSession.builder.getOrCreate()


spark = (SparkSession.builder
                     .appName("Counting word occurences from a book.")
                     .getOrCreate())

df = spark.read.csv("./data_pipeline/preprocessed/2024_elections_result_by_candidate_uk_parliament.csv", inferSchema=True, header=True)
columns = df.columns
columns_lower_snake = [x.lower().replace(" ", "_") for x in columns]

df = df.toDF(*columns_lower_snake)

window_spec = Window.partitionBy("constituency_name").orderBy(F.col("votes").desc())

df_with_rank = df.withColumn("rank", F.row_number().over(window_spec))

df_winner = df_with_rank.filter(F.col("rank") == 1).drop("rank")

df_winner.write.json("./data_pipeline/processed/election_winners.json", mode="overwrite")

json_data = df_winner.toJSON().collect()
#strs to dicts
parsed_data = [json.loads(item) for item in json_data]
output_dictionary = {}

for dictionary in parsed_data:
    if output_dictionary.get(dictionary['ons_id']) == None:
        output_dictionary[dictionary['ons_id']] = {"first": dictionary}
    else:
        output_dictionary[dictionary['ons_id']]["second"] = dictionary

with open("data_pipeline/processed/marginal_seats.json", "w") as f:
    json.dump(output_dictionary, f, indent=4)


# now we also want json with all candidates

# 1. get spark df

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
import json

spark = SparkSession.builder.getOrCreate()


spark = (SparkSession.builder
                     .appName("Marginal seats.")
                     .getOrCreate())

df = spark.read.csv("./data_pipeline/preprocessed/2024_elections_results_by_candidate_uk_parliament.csv", inferSchema=True, header=True)

# 2. calulate total votes for each constituency and add it to new column, 
    # every row will have this, should be same number across all constituencies



df = df.toDF(*[x.lower().replace(" ", "_") for x in df.columns])
df = df.drop("dc_person_id", "mnis_party_id", "electoral_commission_party_id", "party_abbreviation", "electoral_commission_adjunct_party_id")

#define window to rank candidates within each constituency
window_spec = Window.partitionBy("constituency_name").orderBy(F.col("votes").desc())
ranked_df = df.withColumn("rank", F.row_number().over(window_spec))

#filter top two
top_two_candidates = ranked_df.filter(F.col("rank") <= 2)

#calculate vote difference
vote_diff_df = top_two_candidates.groupBy(
    "constituency_name").agg(
        F.max("votes").alias("first_votes"), 
        F.min("votes").alias("second_votes")
        ).withColumn("vote_diff", 
                     F.col("first_votes") - F.col("second_votes"))

#identify swing seats and add additional roles to match with ranked_df
swing_seats = vote_diff_df.filter(F.col("vote_diff") < 5000).select(
    "constituency_name",
    F.lit("Swing Seat").alias("label"),
    F.col("vote_diff").alias("vote_diff")

)

swing_seats = swing_seats.withColumn("swing_seat", F.when(F.col("swing_seat") == "Swing Seat", True).otherwise(False))


final = top_two_candidates.join(swing_seats, on="constituency_name")

json_data = final.toJSON().collect()

###
# NEW DATASET UK PARLIAMENT
##59th Parliament?!
['Parliament number', 
 'Parliament summoned on', 
 'Parliament dissolved on', 
 'Parliament Wikidata ID', 
 'Parliament London Gazette citation', 
 'Parliament URL', 
 'General election polling date', 
 'General election is notional', 
 'Total electorate in general election', 
 'Total valid votes in general election', #48253193
 'Total invalid votes in general election', #116253
 'General election URL', 
 'Country name', #scotland etc
 'Country geographic code', #maybe #W92000004 #Drop
 'Country URL', 

 'English region name', #e.g. 'southeast' #KEEP
 'English region geographic code', #e.g. E12000008
 'English region URL', 

 'Constituency name', #KEEP

 'Constituency geographic code', #e.g. S14000063 # KEEP
 'Constituency designation', #county,burgh borough
 'Constituency URL', 
 'Boundary set start date', #All same
 'Boundary set end date', #all null
 'Boundary set URL', 
['English region name','English region geographic code','Constituency name',
 'Constituency geographic code', 'Constituency designation', 'Electorate', 'Election valid vote count',
 'Election invalid vote count', 'Election result summary', 'Candidate family name', 'Candidate given name',
 'Candidate MNIS ID', 'Candidate is sitting MP', 'Candidate is former MP', 'Main party abbreviation',
 'Candidate is standing as independent', 'Candidate vote count','Candidate vote share', 'Candidate vote change',
 'Majority',
 'Candidate result position'
 ]
 'Electorate', #crucial
 'Election polling date', 
 'Election is by-election', 
 'Declaration time', #all null

 'Election valid vote count', #crucial

 'Election invalid vote count', #crucial
 'Election URL', 

 'Election result summary', #crucial
 'Candidate family name', #join v #change to candidate_name
 'Candidate given name', #join ^
 'Candidate MNIS ID', 

 'Candidate is sitting MP', #keep #change to sitting mp
 'Candidate is former MP', #keep #change to former mp
 'Candidate Member URL', 

 'Main party name', 
 'Main party abbreviation', #crucial #change to 'party'
 'Main party MNIS ID', 
 'Main party URL', 
 'Adjunct party name', 
 'Adjunct party abbreviation', 
 #'Candidate is standing as Commons Speaker', 
 'Candidate is standing as independent', 
 'Candidate vote count', #crucial
 'Candidate vote share', #keep
 'Candidate vote change', #keep
 'Majority', #keep
 'Candidate result position']



# Add to this sum of candidates for each then write to csv
# find if all nulls are independents
# assumed abbreviation is equal
y = df.select(F.col('Main party name'), F.col('Main party abbreviation'), F.col('Main party MNIS ID'),F.col('Main party URL'),F.col('Adjunct party name'),F.col('Adj
unct party abbreviation')).distinct().orderBy(F.col('Main party name').desc())


# scenario 1: base case. if election vote preference were directly correlated to party approval
    # scenario weighted to july 2024. 
    # apply + or - votes to see effect.

# scenario 2: estimate floating voters. 10% drift from labour - split this 33/33/33 amongst other 3 big parties

#The 2023 boundary review was stricter than previous ones in this respect. Constituencies must now have an electorate within 5% of the ‘electoral quota’ – now set at 73,393 registered voters - with just a few exceptions.
{
    id: {
        region_id.
        constituency_name.
        region_name,
        country_name,
        elected_party: [electoral_commission_id]
        ~~swing_from_2019,
        marginal_seat:
        vote_margins:
            [1st_2nd,
            2nd_3rd,
            3rd_4th],
        ~~parties_ranked: [1_id, 2_id]
        results_2024:
            [data: {
                turnout
                turnout_%
            }    
            winner: {
                full_name,
                gender,
                sitting_mp,
                former_mp,
                votes 
                share,
                change,
                party_id,
            },
            second: {

            }]
    }
}


# all parties names

+------------------------------------------------------+
|Main party name                                       |
+------------------------------------------------------+
|Workers Revolutionary Party                           |
|Workers Party of Britain                              |
|Women's Equality Party                                |
|Volt United Kingdom                                   |
|Ulster Unionist Party                                 |
|UK Voice                                              |
|UK Independence Party                                 |
|True & Fair Party                                     |
|Transform Party                                       |
|Traditional Unionist Voice                            |
|Trade Unionist and Socialist Coalition                |
|The Yoruba Party in the UK                            |
|The Yorkshire Party                                   |
|The Socialist Party of Great Britain                  |
|The Peace Party                                       |
|The North East Party                                  |
|The Mitre TW9                                         |
|The Common People                                     |
|Taking The Initiative Party                           |
|Swale Independents                                    |
|Stockport Fights Austerity No To Cuts                 |
|Sovereignty                                           |
|South Devon Alliance                                  |
|Socialist Labour Party                                |
|Socialist Equality Party                              |
|Social Justice party                                  |
|Social Democratic Party                               |
|Social Democratic & Labour Party                      |
|Sinn Féin                                             |
|Shared Ground                                         |
|Scottish Socialist Party                              |
|Scottish National Party                               |
|Scottish Libertarian Party                            |
|Scottish Green Party                                  |
|Scottish Family Party                                 |
|Save Us Now                                           |
|Rejoin EU                                             |
|Reform UK                                             |
|Rebooting Democracy                                   |
|Putting Crewe First, Independent Residents Group      |
|Psychedelic Movement                                  |
|Propel                                                |
|Portsmouth Independent Party                          |
|Plaid Cymru                                           |
|People Before Profit Alliance                         |
|Party of Women                                        |
|One Leicester                                         |
|Official Monster Raving Loony Party                   |
|Newham Independents Party                             |
|New Open Non-Political Organised Leadership           |
|National Health Action Party                          |
|Liverpool Community Independents                      |
|Lincolnshire Independents                             |
|Libertarian Party                                     |
|Liberal Democrat                                      |
|Liberal                                               |
|Labour                                                |
|Kingston Independent Residents Group                  |
|Independents for Direct Democracy                     |
|Independent Oxford Alliance                           |
|Independent Network                                   |
|Independent Alliance (Kent)                           |
|Independence for Scotland Party                       |
|Heritage Party                                        |
|Hampshire Independents                                |
|Green Party Northern Ireland                          |
|Green Party                                           |
|Freedom Alliance                                      |
|Fairer Voting Party                                   |
|English Democrats                                     |
|English Constitution Party                            |
|Democratic Unionist Party                             |
|Democracy for Chorley                                 |
|Cross-Community Labour Alternative                    |
|Count Binface Party                                   |
|Conservative                                          |
|Consensus                                             |
|Confelicity                                           |
|Communist Party of Britain                            |
|Communist League Election Campaign                    |
|Communist Future                                      |
|Common Good Party                                     |
|Climate Party                                         |
|Christian Peoples Alliance Party                      |
|Christian Party, Proclaiming Christ's Lordship        |
|Chesterfield And North Derbyshire Independents (CANDI)|
|British Unionist Party B.U.P.                         |
|British Democratic Party                              |
|Blue Revolution                                       |
|Ashfield Independents                                 |
|Aontú                                                 |
|Animal Welfare Party                                  |
|Alliance for Green Socialism                          |
|Alliance for Democracy and Freedom                    |
|Alliance                                              |
|Alba Party                                            |
|Abolish the Welsh Assembly Party                      |
|null                                                  |
+------------------------------------------------------+