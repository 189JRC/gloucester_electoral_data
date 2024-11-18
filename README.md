### Scaffolding for Web Application

#### Purpose: A Containerised full web application. Starting point for any future website building. 

Flask backend, vue/nginx frontend and postgres db.

#### Local Development.

Start flask development server:
- cd /backend
- python3 app.py

Start Vite front end development server:
- cd /frontend
- npm install -i
- npm run build
- npm run dev

backend accessible on http://0.0.0.0:5000
frontend accessible on http://0.0.0.0:8080

#### Testing for production.

In root directory
- docker-compose build --no-cache
- docker-compose up

backend accessible on http://0.0.0.0:5000
frontend accessible on http://0.0.0.0:8080

#### Deployment to a remote server.

Connection to remote server instance required.
SSH <ip-address> etc...

- (For now) copy files across with scp.
- docker-compose build --no-cache
- docker-compose up

backend accessible on http://<server-ip>:5000
frontend accessible on http://<server-ip>:8080

TODO: make sample github actions file to allow for one click deployment and setup
TODO: comment on nginx.conf to show more detail on configuration options
TODO: setup a fetch call from App.vue to ensure connection (and that db read/write can happen from frontend)
TODO: include gunicorn server option as well as flask development server
TODO: create a sample .env file

~~~~~~~~~~~~~~~~~~~~

please make this into json data with the format
{
"ward name" (e.g. Westgate):
     "leave votes": int,
     "leave percentage": str,
    "remain votes": int,
    "remain percentage": int,
    "total votes": int,
    "electorate": int,
}

DO NOT MAKE ANY VALUES UP. IF THERE IS AMBIGUITY YOU NEED TO TELL ME


In geojson:
EW1: WD24CD - Electoral Ward 2024

IMD data:
IMD1: LSOA2011 - Lower Layer Super Output Areas 2011

Need to map LSOA2011 to EW24

ONS:
LU1: can map LSOA2011 -> LSOA21
LU2: can map LSOA2021 -> WD24CD

- start psql container
- script to take csv and add:
LU1, LU2, IMD1, EW1
SELECT LSOA11CD, LSOA21 FROM LU1 WHERE LAD22NM = Gloucester;

.mode csv
.import <--skip 1> filename.csv tablename

.output /path/to/your/joined_lsoa_wd.csv
.output stdout

CREATE TABLE joined_imd_lsoa11_wd24 AS
SELECT 
    imd_2019.LSOA AS lsoa11_id,
    imd_2019.LANAME AS local_authority_name,
    imd_2019.RANK AS absolute_deprivation_ranking, (highest is least deprived, 1 is least)
    imd_2019.SOA_pct AS relative_deprivation_ranking_pct, (most deprived 1% is 1, least is 100)
    imd_2019.SOA_decile AS deprivation_decile, (most deprived 10% is 1)
    imd_2019.LA_Rank AS local_authority_rank, (ranking for local auth, all should be the same)
    imd_2019.LA_pct AS local_authority_rank_pct,
    imd_2019.LA_decile AS local_authority_decile,
    joined_lsoa_wd.lsoa11cd AS lsoa11cd_id, (these should all match)
    joined_lsoa_wd.lad22nm AS lad22nm,
    joined_lsoa_wd.wd_lsoa21cd AS lsoa21cd,
    joined_lsoa_wd.lsoa21nm AS lsoa21nm,
    joined_lsoa_wd.wd24cd AS wd24cd,
    joined_lsoa_wd.wd24nm AS wd24nm
FROM 
    imd_2019
JOIN
    joined_lsoa_wd
ON
    imd_2019.LSOA = joined_lsoa_wd.lsoa11cd;




CREATE TABLE joined_imd_lsoa11_wd24 AS
SELECT 
    imd_2019.LSOA AS lsoa11_id,
    imd_2019.LANAME AS local_authority_name,
    imd_2019.RANK AS absolute_deprivation_ranking,
    imd_2019.SOA_pct AS relative_deprivation_ranking_pct,
    imd_2019.SOA_decile AS deprivation_decile,
    imd_2019.LA_Rank AS local_authority_rank,
    imd_2019.LA_pct AS local_authority_rank_pct,
    imd_2019.LA_decile AS local_authority_decile,
    joined_lsoa_wd.lsoa11cd AS lsoa11cd_id,
    joined_lsoa_wd.lad22nm AS lad22nm,
    joined_lsoa_wd.wd_lsoa21cd AS lsoa21cd,
    joined_lsoa_wd.lsoa21nm AS lsoa21nm,
    joined_lsoa_wd.wd24cd AS wd24cd,
    joined_lsoa_wd.wd24nm AS wd24nm
FROM 
    imd_2019
JOIN
    joined_lsoa_wd
ON
    imd_2019.LSOA = joined_lsoa_wd.lsoa11cd;


SELECT 
    wd24nm,
    AVG(relative_deprivation_ranking_pct) AS avg_absolute_deprivation_pct
FROM 
    final_table
GROUP BY 
    wd24nm;

wd24nm|avg_absolute_deprivation_pct
Abbeydale|74.25
Abbeymead|82.6666666666667
Barnwood|78.6666666666667
Barton and Tredworth|16.2857142857143
Coney Hill|18.6666666666667
Elmbridge|73.0
Grange|56.75
Hucclecote|80.0
Kingsholm and Wotton|28.75
Kingsway|56.0
Longlevens|86.8333333333333
Matson, Robinswood and White City|18.5714285714286
Moreland|29.4285714285714
Podsmead|24.5
Quedgeley Fieldcourt|62.0
Quedgeley Severn Vale|81.25
Tuffley|43.5
Westgate|21.0