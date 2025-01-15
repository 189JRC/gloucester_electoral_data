<template>
    <div class="flex justify-center mt-2 border-gray-500">
        
    </div>
    <div class="flex mt-5">
        <div class="flex-col justify-center w-1/3 px-5">
            <div id="ward-name" class="flex-1">
                <div v-if="show_election_datacard" class="border-4 border-gray-700 text-xl p-5 text-center">
                    <br>
                    <ElectionDataCard :selected_constituency="selected_constituency"
                        @update-seat-threshold="updated_margin" @turnout-threshold-changed="updated_turnout" />
                </div>
            </div>
            <button @click="reset_constituency_map" class="text-3xl mt-4 p-2 bg-gray-100 border-2 border-black mx-2">
                Reset Map</button>
        <button @click="change_colour_setting" class="text-3xl mt-4 p-2 bg-gray-100 border-2 border-black mx-2">
            <span v-if="colour_setting">Neutralise Colours</span>
            <span v-if="!colour_setting">Show Party Colours</span>
        </button>
        </div>
        
        <div class="flex-1 h-1/2 w-1/2 px-5">
            <div class="ml-12">
                <!-- The viewBox should start at (cx - rx, cy - ry) and extend to (width, height) -->
                <svg ref="map" width="1325" height="1325" viewBox="10 0 900 900">
                </svg>
            </div>
            <div id="tooltip"
                style="position: absolute; visibility: hidden; background: white; padding: 5px; border: 1px solid black;">
            </div>
        </div>
        <div class="flex-col justify-center w-1/3 px-5">
            <div id="ward-name" class="flex-1">
                <div v-if="show_election_datacard" class="border-4 border-gray-700 text-xl p-5 text-center">
                    <br>
                    <ConstituencyDataCard v-if="show_election_datacard" :selected_constituency="selected_constituency"
                        :show_margin_scale="show_margin_scale" />
                    <!-- :seat_count="seat_count" -->
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
import party_mapping from '@/js_object_data/party_mapping.json';
import { area } from 'd3';
import ConstituencyDataCard from './ConstituencyDataCard.vue';
import ElectionDataCard from './ElectionDataCard.vue';

export default {
    components: {
        ConstituencyDataCard,
        ElectionDataCard
    },
    data() {
        return {
            //Constituency datacard child component
            show_election_datacard: false,
            selected_constituency: null,
            seat_count: null,
            show_margin_scale: false,

            selected_margin: 5000,
            turnout_threshold: 50,
            //other
            colour_setting: true,
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
            this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', this.colour_setting)
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
        async init_constituency_map(
                geo_data, 
                election_winners, 
                type='election_results', 
                marginal_threshold=5000,
                turnout_threshold=50
            ) {

            // console.log(this.colour_setting)
            const svg = d3.select(this.$refs.map);
            svg.selectAll("path").remove();
            this.projection = d3.geoMercator()
                .center([0.04225, -0.05935])
                .scale(450000)
                .translate([320, 450]);

            this.path = d3.geoPath().projection(this.projection);

            function apply_party_colour(
                                    geodata_reference_point,
                                    candidate_data,
                                    party_mapping,
                                    marginal_threshold,
                                    turnout_threshold,
                                    colour_setting
                                    ) {


                const area_id = geodata_reference_point.properties.id
                if (type === 'election_results') {
                    //this takes winner for each constituency and maps it to find the colour
                    try {
                        return party_mapping[candidate_data[area_id]['winning_party'].toLowerCase()]['colour']
                    } catch {
                        return "grey"
                    }
                    // } else if (type === 'turnout_threshold') {
                    //                 // trying to combine this with majority threshold (else case)
                    //     const turnout = (candidate_data[area_id]['votes_counted']/
                    //                     candidate_data[area_id]['electorate'] *
                    //                 100).toFixed(2)
                    //     if (turnout > marginal_threshold) {
                    //         if (colour_setting === false) {
                    //             return "lightgreen"
                    //         } else {
                    //             return party_mapping[candidate_data[area_id]['winning_party'].toLowerCase()]['colour']
                    //         }
                    //     }
                } else {
                    //get turnout and majority for each seat
                    const majority = candidate_data[area_id]['majority']

                    const turnout = (candidate_data[area_id]['votes_counted'] /
                        candidate_data[area_id]['electorate'] *
                        100).toFixed(2)

                    if (majority < marginal_threshold && turnout < turnout_threshold) {
                        if (colour_setting === false) {
                            return "lightgreen"
                        } else {
                            return party_mapping[candidate_data[area_id]['winning_party'].toLowerCase()]['colour']
                        }

                    } else {
                        return "black"
                    }
                }
            }
            const ctx_party_mapping = this.party_mapping
            const colour_setting = this.colour_setting
            svg.selectAll("path")
                .data(geo_data.features)
                .enter()
                .append("path")
                .attr("class", "constituency")
                .attr("d", this.path)
                .attr("clip-path", "url(#ovalClip)")
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
                    this.scope_test(geo_point, election_winners)
                })
                .style("fill", geo_point =>
                                apply_party_colour(
                                    geo_point,
                                    election_winners,
                                    ctx_party_mapping,
                                    marginal_threshold,
                                    turnout_threshold,
                                    colour_setting
                                ));
        },
        scope_test(geo_point, election_winners) {
            this.selected_constituency = election_winners[geo_point.properties.id]
            this.show_election_datacard = true
        },
        updated_margin(selected_margin) {
            this.selected_margin = selected_margin
            this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', this.selected_margin, this.turnout_threshold)
        },
        updated_turnout(turnout_threshold) {
            this.turnout_threshold = turnout_threshold
            this.init_constituency_map(this.geo_data, this.election_winners, 'turnout_threshold', this.selected_margin, this.turnout_threshold)
        },
        colour_neutralise() {
            this.neutral_colours = !this.neutral_colours
            this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', this.selected_margin, this.turnout_threshold)
        },
        change_colour_setting() {
            if (this.colour_setting === false) {
                this.colour_setting = true
                // this.neutral_colours = false
                this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', this.selected_margin, this.turnout_threshold)
            } else {
                this.colour_setting = false
                // this.neutral_colours = true
                this.init_constituency_map(this.geo_data, this.election_winners, 'marginal_seats', this.selected_margin, this.turnout_threshold)

            }

        }
    },

    watch: {
        // Watch for when both datasets are ready
        // TODO: find a neater way to do this
        election_winners(election_winners_fetched) {
            if (election_winners_fetched && this.geo_data) {
                this.init_constituency_map(election_winners_fetched, this.geo_data);
                this.scope_test(this.geo_data['features'][0], election_winners_fetched)
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
