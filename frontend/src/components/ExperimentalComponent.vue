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
                    <ConstituencyDataCard v-if="show_election_datacard" 
                    :selected_constituency="selected_constituency"
                    
                    :show_margin_scale="show_margin_scale"
                    @selected-margin-changed="updated_margin"/>
                    <!-- :seat_count="seat_count" -->
                </div>
            </div>
            <!-- <div class="flex flex-row">
                
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
            </div> -->
        </div>
    </div>
    <div class="flex justify-center items-center">
        <div class="border-2 w-1/2 border-gray-300 rounded-lg mt-5">
        </div>
    </div>
</template>

<script>
import * as d3 from 'd3';
import party_mapping from '@/js_object_data/party_mapping.json';
import { area } from 'd3';
import ConstituencyDataCard from './ConstituencyDataCard.vue';

export default {
    components: {
        ConstituencyDataCard
    },
    data() {
        return {
            //Constituency datacard child component
            show_election_datacard: false,
            selected_constituency: null,
            seat_count: null,
            show_margin_scale: false,
            //other
            party_mapping,
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
        // Grab data needed for map rendering
        // When these are available the watch function triggers map init
        this.fetch_candidate_results_json()
        this.fetch_geo_data()
    },
    methods: {
        count_party_seats(election_winners) {
            // get list of all parties with their full name mapping
            const seat_count = {}
            Object.entries(election_winners).forEach(([location_id, election_results]) => {
                    if (seat_count[election_winners[location_id]['winning_party']]) {
                        seat_count[election_winners[location_id]['winning_party']] += 1
                    } else {
                        seat_count[election_winners[location_id]['winning_party']] = 1
                    }
                });
                this.seat_count = seat_count
            },
        apply_marginal_seats() {
            this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats')
            this.show_margin_scale = true
        },
        async fetch_candidate_results_json() {
            //Fetch election data for rendering onto hexmap
            const response = await fetch("/2024_candidates_symlink")
            this.election_winners = await response.json()
        },
        async fetch_geo_data() {
            //Fetch geodata to allow hexmap rendering
            const response = await fetch("/constituencies_2024.geojson")
            this.geo_data = await response.json()
        },
        async reset_constituency_map() {
            this.init_constituency_map(this.geo_data, this.election_winners)
            this.count_party_seats(this.election_winners)
        },
        async init_constituency_map(geo_data, election_winners, type = 'election_results', marginal_threshold=5000) {
            console.log(type)
            const svg = d3.select(this.$refs.map);
            svg.selectAll("path").remove();
            this.projection = d3.geoMercator()
                .center([0.04225, -0.05935])
                .scale(455000)
                .translate([400, 500]);

            this.path = d3.geoPath().projection(this.projection);

            function apply_party_colour(geodata_reference_point, candidate_data, party_mapping, marginal_threshold) {
                const area_id = geodata_reference_point.properties.id
                if (type === 'election_results') {
                    //this takes winner for each constituency and maps it to find the colour
                    try {
                        return party_mapping[candidate_data[area_id]['winning_party'].toLowerCase()]['colour']
                    } catch {
                        return "grey"
                    }
                } else {
                    const majority = candidate_data[area_id]['majority']
                    console.log(marginal_threshold)
                    if (majority < marginal_threshold) {
                        return "lightgreen"
                    } else {
                        return "grey"
                    }
                    console.log("HI", candidate_data[area_id]['majority'], party_mapping)
                    return "green"
                // } else {
                    // try {
                        // console.log(geodata_reference_point[area]['first'])
                        // const majority = geodata_reference_point
                        // console.log(majority)
                        // // const greenShades = ["#d4f7d4", "#a8e6a8", "#74d474", "#3fc13f", "#1a9d1a"];
                        // if (voteDiff < 1000) {
                        //     return greenShades[0]; // Lightest green
                        // }
                        // if (voteDiff < 2000) {
                        //     return greenShades[1];
                        // }
                        // if (voteDiff < 3000) {
                        //     return greenShades[2];
                        // }
                        // if (voteDiff < 4000) {
                        //     return greenShades[3];
                        // }
                        // if (voteDiff < 5000) {
                        //     return greenShades[4]; // Darkest green
                        // }
                        // if (voteDiff < 10000) {
                        //     return 'orange'; // Darkest green
                        // }
                    //     return "lightgrey"; // Default for other cases
                    // } catch {
                    //     return "lightgray"
                    // }
                }
            }
            const ctx_party_mapping = this.party_mapping
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
                .style("fill", geo_point => apply_party_colour(geo_point, election_winners, ctx_party_mapping, marginal_threshold));
        },
        scope_test(event, geo_point, election_winners, type) {
            //geo_point.properties.id is this constituency id
            this.selected_constituency = election_winners[geo_point.properties.id]            
            this.show_election_datacard = true

            // this.marginals_datacard = null

            // if (type === "election_results") {
            //     const winner_details = election_winners[geo_point.properties.id]
            //     this.election_datacard = winner_details
            // } else {
            //     const winner_details = election_winners[geo_point.properties.id]
            //     console.log(winner_details)
            //     this.marginals_datacard = winner_details
            // }
        },
        updated_margin(val) {
            console.log("264", val)
            this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', val)
        }
    },

    watch: {
        // Watch for when both datasets are ready
        // TODO: find a neater way to do this
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
