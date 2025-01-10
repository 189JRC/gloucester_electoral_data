<template>
    <div class="flex mt-5">

        <div class="flex-1 h-1/2 w-1/3 px-5 mx-auto">
            <div class="border-2 border-gray-300 bg-gray-50 mt-5">
                <svg ref="map" width="1200" height="800"></svg>
            </div>
            <div id="tooltip"
                style="position: absolute; visibility: hidden; background: white; padding: 5px; border: 1px solid black;">
            </div>
            <div class="flex justify-center mt-2 border-gray-500">
                <button @click="reset_constituency_map"
                    class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl ">General Election Results</button>
                <button @click="apply_marginal_seats"
                    class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl ">Marginals Seats</button>
            </div>
        </div>
        <div class="flex-col justify-center w-1/2 px-5">
            <div id="ward-name" class="flex-1">
                <div class="border-4 border-gray-700 text-xl p-5 text-center">
                    <br>
                </div>
            </div>
            <div class="flex flex-row">
                <div id="council-election-results" class="flex-1">
                    <div class="mt-5 text-center border-l border-b border-t border-gray-700 text-xl py-2">
                    </div>

                    <div class="border-l border-gray-700 pl-3 py-2">
                    </div>

                    <hr class="border-t-3 border-gray-500">

                    <div>
                        <div v-if="election_datacard" class="text-center border-l border-b border-gray-700 text-xl">
                            <strong>Elections Results</strong><br>
                            <div v-for="(label, key) in mapping" :key="key" class="text-left">
                                <strong>{{ label }}:</strong> {{ election_datacard[key] }}
                            </div>
                        </div>
                        <div v-if="marginals_datacard" class="text-center border-l border-b border-gray-700 text-xl">
                            <strong>Marginals Results</strong><br>
                            <div class="text-left">
                                <div>Constituency: {{ marginals_datacard['first']['constituency_name'] }}</div>
                                <div>Party: {{ marginals_datacard['first']['party_name'] }}</div>
                                <div>2nd place: {{ marginals_datacard['second']['party_name'] }}</div>
                                <div>Margin: {{ marginals_datacard['first']['votes'] }} beat {{ marginals_datacard['second']['votes'] }} </div>
                                <div>Vote diff: {{ marginals_datacard['first']['vote_diff'] }}</div>
                            </div>
   <br>
                            <div class="text-left">
                                {{ marginals_datacard['first'] }}
                            </div>
                            <br>
                            <div class="text-left">
                                {{ marginals_datacard['second'] }}
                            </div>
                        </div>
            
                        <div class="overflow-auto max-h-1/2" style="height: 50vh;">

                        </div>
                    </div>
                </div>
                <div id="brexit-referendum-results" class="flex-1">
                </div>
            </div>
        </div>
    </div>
    <div class="flex justify-center items-center">
        <div class="border-2 w-1/2 border-gray-300 rounded-lg mt-5">
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';

export default {
    data() {
        return {
            marginals_datacard: null,
            election_datacard: null,
            election_winners: null,
            geo_data: null,
            projection: null,
            mapping: {
                ons_region_id: "ONS Region ID",
                constituency_name: "Constituency Name",
                region_name: "Region Name",
                constituency_type: "Constituency Type",
                party_name: "Party Name",
                candidate_first_name: "Candidate First Name",
                candidate_surname: "Candidate Surname",
                candidate_gender: "Candidate Gender",
                sitting_mp: "Sitting MP",
                former_mp: "Former MP",
                votes: "Votes",
                share: "Vote Share"
            }
        };
    },
    mounted() {
        this.fetch_election_winners()
        this.fetch_geo_data()
    },
    methods: {
        async apply_marginal_seats() {
            this.election_datacard = null
            const response = await fetch("/marginal_seats.json")
            const marginals = await response.json()
            console.log(marginals)
            this.init_constituency_map(this.geo_data, marginals, 'marginal_seats')
        },
        async fetch_election_winners() {
            const response = await fetch("/election_winners.json")
            this.election_winners = await response.json()
        },
        async fetch_geo_data() {
            const response = await fetch("/constituencies_2024.geojson")
            this.geo_data = await response.json()
        },
        async reset_constituency_map() {
            this.init_constituency_map(this.geo_data, this.election_winners)
        },
        async init_constituency_map(geo_data, election_winners, type='election_results') {
            console.log("HIT")
            const svg = d3.select(this.$refs.map);
            svg.selectAll("path").remove();
            this.projection = d3.geoMercator()
                .center([0.04225, -0.05935])
                .scale(455000)
                .translate([400, 500]);

            this.path = d3.geoPath().projection(this.projection);

            function apply_party_colour(d, e) {
                // if (geo_data.properties.id === election_winners.)
                const area = d.properties.id
                if (type === 'election_results') {
                    if (e[area]['party_name'] == 'Labour' || e[area]['party_name'] == 'Labour and Co-operative') {
                        return 'red'
                    } else if (e[area]['party_name'] == 'Conservative') {
                        return 'blue'
                    } else if (e[area]['party_name'] == 'Reform UK') {
                        return 'lightblue'
                    } else if (e[area]['party_name'] == 'Liberal Democrat') {
                        return 'orange'
                    } else if (e[area]['party_name'] == 'Plaid Cymru') {
                        return 'green'
                    } else if (e[area]['party_name'] == 'Scottish National Party') {
                        return 'yellow'
                    } else if (e[area]['party_name'] == 'Green') {
                        return 'lightgreen'
                    } else if (e[area]['party_name'] == 'Speaker') {
                        return 'black'
                    } else {
                        // console.log(e[area]['party_name'])
                        return 'grey'
                    }
                } else {
                    try{
                        console.log(e[area]['first'])
                        const voteDiff = e[area]['first']['vote_diff']
                        const greenShades = ["#d4f7d4", "#a8e6a8", "#74d474", "#3fc13f", "#1a9d1a"];
                        if (voteDiff < 1000) {
                            return greenShades[0]; // Lightest green
                        } 
                        if (voteDiff < 2000) {
                            return greenShades[1];
                        }
                        if (voteDiff < 3000) {
                            return greenShades[2];
                        }
                        if (voteDiff < 4000) {
                            return greenShades[3];
                        }
                        if (voteDiff < 5000) {
                            return greenShades[4]; // Darkest green
                        } 
                        if (voteDiff < 10000) {
                            return 'orange'; // Darkest green
                        } 
                        return "lightgrey"; // Default for other cases
                    } catch {
                        return "lightgray"
                    }
                }
            }

            svg.selectAll("path")
                .data(geo_data.features)
                .enter()
                .append("path")
                .attr("class", "constituency")
                .attr("d", this.path)
                .style("fill", "gray")
                .style("stroke", "white")
                .style("stroke-width", 0.5)
                .on("mouseover", function (event, geo_data) {
                    d3.select(this).style("stroke-width", 2.5);
                    const tooltip = document.getElementById('tooltip');
                    tooltip.style.visibility = 'visible';
                    tooltip.innerHTML = geo_data.properties.n; // Show ward name
                    tooltip.style.left = event.pageX + 10 + 'px';
                    tooltip.style.top = event.pageY + 10 + 'px';
                })
                .on("mouseout", function (event, geo_data) {
                    d3.select(this).style("stroke-width", 0.5)
                })
                .on("click", (event, geo_point) => {
                    this.scope_test(event, geo_point, election_winners, type)
                })
                .style("fill", geo_point => apply_party_colour(geo_point, election_winners));
        },
        scope_test(event, geo_point, election_winners, type) {
            // console.log(election_winners)
            this.election_datacard = null 
            this.marginals_datacard = null

            if (type === "election_results") {
                const winner_details = election_winners[geo_point.properties.id]
                this.election_datacard = winner_details
            } else {
                const winner_details = election_winners[geo_point.properties.id]
                console.log(winner_details)
                this.marginals_datacard = winner_details
            }
        }
    },

    watch: {
        // Watch for when both datasets are ready
        election_winners(election_winners_fetched) {
            if (election_winners_fetched && this.geo_data) {
                this.init_constituency_map(election_winners_fetched, this.geo_data);
            }
        },
        geo_data(geo_data_fetched) {
            if (geo_data_fetched && this.election_winners) {
                this.init_constituency_map(geo_data_fetched, this.election_winners);
            }
        }
    }

}
</script>