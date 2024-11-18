<template>
    <div class="flex mt-5">
        
        <div class="flex-1 h-1/2 w-1/3 px-5 mx-auto">  
            <div class="border-4 border-gray-700 text-xl p-5 text-center">
                <span v-if="title_for_ward_map==='ward'"><strong>Gloucester Council Ward Map</strong></span>
                <span v-if="title_for_ward_map==='brexit'"><strong>Gloucester Referendum Results by Ward</strong> (Leave Vote %)</span>
                <span v-if="title_for_ward_map==='deprivation'"><strong>Gloucester: <a href="https://data.cdrc.ac.uk/dataset/index-multiple-deprivation-imd" class="text-blue-500">Index for Multiple Deprivation</a></strong></span>
            </div>
            <div class="border-2 border-gray-300 bg-gray-50 mt-5">
                <svg ref="map" width="1000" height="600"></svg>
            </div>
            <div id="tooltip"
                style="position: absolute; visibility: hidden; background: white; padding: 5px; border: 1px solid black;">
            </div>
            <div class="flex justify-center mt-2 border-gray-500">
            
            <button class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl " @click="apply_brexit_layer_to_map"><strong>Referendum results</strong></button>
            <button class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl  " @click="initMap"><strong>Council Election Results</strong></button>
            <button class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl" @click="init_poverty_map"><strong>Relative Deprivation</strong></button>
            <button class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl" @click="neutralise"><strong>Neutralise Map Colours</strong></button>
            </div>
        </div>
        
        
        <div class="flex-col justify-center w-1/2 px-5">
            <div id="ward-name" class="flex-1">
                <div class="border-4 border-gray-700 text-xl p-5 text-center">
                    <strong v-if="ward_election_datacard">{{ ward_election_datacard['Ward'] }} Ward</strong>
                    <strong v-if="!ward_election_datacard">Select a Ward on Map to View Election Data</strong>
                    <br>
                </div>
            </div>
            <div class="flex flex-row">
                <div id="council-election-results" v-if="ward_election_datacard" class="flex-1">
                    
                    <div class="mt-5 text-center border-l border-b border-t border-gray-700 text-xl py-2">
                        <strong>Last Council Election: </strong>{{ new Date(ward_election_datacard['Previous Election']).toLocaleDateString('en-UK', { day: '2-digit', month: 'short', year: 'numeric' }) }}
                    </div>
                    
                    <div class="border-l border-gray-700 pl-3 py-2">
                        <strong>Turnout: </strong>{{ ward_election_datacard['Turnout %'] }}<br>
                    <strong>Electorate: </strong>{{ ward_election_datacard['Electorate'] }} eligible voters<br>
                    <strong>Votes Cast: </strong>{{ ward_election_datacard['Votes'] }}<br>
                    </div>
                    
                    <hr class="border-t-3 border-gray-500">

                    <div>
                        <div class="text-center border-l border-b border-gray-700 text-xl"><strong>Results</strong><br></div>
                        <div class="overflow-auto max-h-1/2" style="height: 50vh;">
                        <div v-for="(result, key) in ward_election_datacard['Results']" :key="key">
                            <div :class="{
                                'bg-blue-700 text-white': result[key + 1].Outcome === 'Elected' && result[key + 1].Party.includes('Conservative'),
                                'bg-yellow-400 text-black': result[key + 1].Outcome === 'Elected' && result[key + 1].Party.includes('Liberal Democrat'),
                                'bg-red-500 text-black': result[key + 1].Outcome === 'Elected' && result[key + 1].Party.includes('Labour'),
                                'bg-orange-400 text-black': result[key + 1].Outcome === 'Elected' && result[key + 1].Party.includes('Independent'),
                                'bg-gray-500 text-black': result[key + 1].Outcome === 'Not elected',
                                'py-2': true
                                
                                
                            }">
                                <strong class="pl-3">Candidate:</strong> {{ result[key + 1].Candidate }}<br>
                                <strong class="pl-3">Party:</strong> <span :class="{
                                    'bg-green-600': result[key + 1].Party.includes('Green'),
                                    'bg-blue-700 text-white': result[key + 1].Party.includes('Conservative'),
                                    'bg-yellow-400 text-black': result[key + 1].Party.includes('Liberal'),
                                    'bg-red-500 text-black': result[key + 1].Party.includes('Labour'),
                                    'bg-red-700 text-black': result[key + 1].Party.includes('Socialist'),
                                    'bg-orange-400 text-black': result[key + 1].Party.includes('Independent'),

                                }">{{ result[key + 1].Party }}</span><br>
                                <strong class="pl-3">Votes:</strong> {{ result[key + 1].Votes }}<br>
                                <strong class="pl-3">Outcome:</strong> {{ result[key + 1].Outcome }} ({{ result[key + 1].Percentage
                                }})<br>
                                
                            </div>
                            <hr>
                        </div>
                    </div>
                    </div>
                </div>
                <div id="brexit-referendum-results" class="flex-1">
                    <div v-if="ward_election_datacard" :class="{
                        'bg-[rgba(100,150,150,1)]': brexit_election_datacard['colour'] === 'rgba(100, 150, 150, 1)',
                        'bg-[rgba(59,145,204,0.8)]': brexit_election_datacard['colour'] === 'rgba(59, 145, 204, 0.9)',
                        'bg-[rgba(40,109,156,0.6)]': brexit_election_datacard['colour'] === 'rgba(40, 109, 156, 0.5)',
                        'bg-[rgba(18,77,117,0.4)]': brexit_election_datacard['colour'] === 'rgba(18, 77, 117, 0.3)',
                        'bg-[rgba(19,59,87,0.2)]': brexit_election_datacard['colour'] === 'rgba(19, 59, 87, 0.1)',
                        'bg-orange-500': brexit_election_datacard['colour'] === 'orange',
                        'bg-red-500': brexit_election_datacard['colour'] === 'red'
                    }">

                        <div class="mt-5 text-center border-l border-b border-t border-r border-gray-700 text-xl py-2 bg-white">
                            <strong>Brexit Referendum: </strong>23 Jun 2016
                        </div>
                        
                        
                        <div class="border-l border-gray-700 pl-3 py-2 bg-white border-r">
                            <strong>Turnout: </strong>{{ brexit_election_datacard['turnout_percentage'] }}%<br>
                        <strong>Electorate: </strong>{{ brexit_election_datacard['electorate'] }} eligible voters<br>
                        <strong>Votes Cast: </strong>{{ brexit_election_datacard['total_votes'] }} <br> 
                        </div>
                        
                        <hr class="border-t-3 border-gray-500">
                        <div class="text-center bg-white border-l border-b border-r border-gray-700 text-xl text-center mr-0">
                            <strong>Results</strong><br></div>
                        <div class="pl-3 py-2">
                            <strong>Votes Leave: </strong>{{ brexit_election_datacard['leave_votes'] }}<br>
                        <strong>Votes Remain: </strong>{{ brexit_election_datacard['remain_votes'] }}<br>
                        <strong>Leave: </strong>{{ brexit_election_datacard['leave_percentage'] }}%<br>
                        <strong>Remain: </strong>{{ brexit_election_datacard['remain_percentage'] }}%<br>
                        </div>
                        <div class="mt-5 text-center border-l border-b border-t border-r border-b border-gray-700 text-xl py-2 bg-white">
                            <strong>Relative Deprivation: </strong>
                        </div>
                        
                        
                        <div @click="show_areas" class="border-l border-b border-gray-700 pl-3 py-2 bg-white border-r">
                            <strong>Areas: </strong>{{imd_ward_datacard.areas}}<br>
                            <strong>Mean Deprivation Ranking: </strong>{{ Math.round(imd_ward_datacard.mean_absolute_deprivation_ranking * 10) / 10 }}%<br>
                            <i class="text-gray-700">NOTE: Lower number indicates a higher relative deprivation</i><br>
                        </div>
                        <div v-if="show_deprivation_areas">
                            <div v-for="(lsoa_info, key) in imd_ward_datacard['other_area_info']" :key="key" class="pl-3 border-l border-b border-r border-gray-700 bg-gray-100">
                            Area ID: {{lsoa_info.lsoa11_id}}<br>
                            Area Ranking: {{ lsoa_info['absolute_deprivation_ranking'] }}<br>
                            Deprivation Decile: {{ lsoa_info['deprivation_decile'] }}
                            </div>
                        </div>
                            

                        
                    </div>
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
import { text } from 'd3';

export default {
    data() {
        return {
            projection: null,
            path: null,
            data: 0,
            selected_json: 0,
            selected_json_datacard: null,
            election_data: 1,
            ward_election_datacard: 0,
            brexit_election_datacard:0,
            imd_ward_datacard: 0,
            brexit_data: 0,
            deprivation_data: 0,
            ld_colour: 'rgba(250,200,0,0.8)',
            space_filler_no_ward_selected: false,
            title_for_referendum: false,
            title_for_ward_map: false,
            show_deprivation_areas: false
        };
    },
    mounted() {
        this.fetch_ward_results_by_name("");
        this.initMap();
        //this.init_poverty_map();
        // this.json_test();
        this.fetch_brexit_results();
        this.fetch_imd_data();
    },
    methods: {
        show_areas() {
            this.show_deprivation_areas = !this.show_deprivation_areas
        },
        reformat_key() {
            const text_elements = Array.from(this.$refs.map.querySelectorAll('text'));
            for (let i=0;i<text_elements.length;i++) {
                text_elements[i].innerHTML = ""
                if (i > 3) {
                    text_elements[i].remove();
                }
            }
            const key_elements = Array.from(this.$refs.map.querySelectorAll('rect'));
            for (let i=0;i<key_elements.length;i++) {
                key_elements[i].setAttribute("style", "fill: white")
                if (i > 3) {
                    key_elements[i].remove();
                }
            }
        },
        neutralise() {
            this.reformat_key()
            const pathElements = this.$refs.map.querySelectorAll('path');
            pathElements.forEach(path => {
                path.setAttribute("style", "fill: steelblue; stroke: white; stroke-width: 0.5px;");
            });
            const key_elements = Array.from(this.$refs.map.querySelectorAll('rect'));
            key_elements.forEach(key => {
                key.setAttribute("style", "fill: white")
            })
            },
        get_brexit_colour(d) {
            (d)
            d = d.replace(/\s+/g, '_');
            d = d.replace(/,/g, '');

            switch (true) {
                case this.brexit_data[d]['leave_percentage'] > 80:
                    return "rgba(100, 150, 150, 1)";
                case this.brexit_data[d]['leave_percentage'] > 70:
                    return "rgba(59, 145, 204, 0.9)";
                case this.brexit_data[d]['leave_percentage'] > 60:
                    return 'rgba(40, 109, 156, 0.5)';
                case this.brexit_data[d]['leave_percentage'] > 50:
                    return 'rgba(18, 77, 117, 0.3)';
                case this.brexit_data[d]['leave_percentage'] > 40:
                    return "rgba(19, 59, 87, 0.1)";
                case this.brexit_data[d]['leave_percentage'] > 30:
                    return "orange";
                default:
                    return "rgba(150,150,150,1)";
            }
        },
        async apply_brexit_layer_to_map() {
            this.space_filler_no_ward_selected = false
            this.title_for_ward_map = 'brexit' 
            //this.reformat_key()
            const svg = d3.select(this.$refs.map);
            // Select all path elements in the SVG

            const paths = svg.selectAll("path");
            
            //changes map colours
            const path_elements = Array.from(this.$refs.map.querySelectorAll('path'));

            path_elements.forEach(path => {
                const d = path.__data__;
                //const color = "cyan" //this.get_brexit_colour(d); // Get the color based on the properties
                const colour = this.get_brexit_colour(d.properties.WD24NM)
                const style = `fill: ${colour}; stroke: white; stroke-width: 0.5px;`
                path.setAttribute("style", style) // Set the fill color
            });

            //removes rectangles
            const key_elements = Array.from(this.$refs.map.querySelectorAll('rect'));
            key_elements.forEach(element => {
                element.remove()
            })
            // key_elements[0].style = "fill: rgba(59, 145, 204, 0.9)"
            // key_elements[1].style = "fill: rgba(40, 109, 156, 0.5)"
            // key_elements[2].style = "fill: rgba(18, 77, 117, 0.3)"
            // key_elements[3].style = "fill: rgba(19, 59, 87, 0.1)"

            //removes text
            const text_elements = Array.from(this.$refs.map.querySelectorAll('text'));
            text_elements.forEach(element => {
                element.remove()
            })
            // // text_elements[0].innerHTML = "51-60%"
            // // text_elements[1].innerHTML = "71-80%"
            // // text_elements[2].innerHTML = "61-70%"
            // console.log(text_elements[2].style)
            // const textElements = Object.values(this.$refs).filter(ref => ref.tagName === 'text');

    // Change the fill attribute to black
    // textElements.forEach(textElement => {
    //   d3.select(textElement).attr("fill", "black");
    // });
// Change the fill attribute to black
          
            // text_elements[3].innerHTML = "50%"


            const svg2 = d3.select("svg");
            const brxt_colours = ["rgba(0, 150, 255, 1)",
                                "rgba(59, 145, 204, 0.8)",
                                'rgba(40, 109, 156, 0.5)',
                                'rgba(18, 77, 117, 0.3)',
                                "rgba(19, 59, 87, 0.1)",
                                "rgba(206, 186, 186, 0.8)",
                                "rgba(206, 149, 149, 0.8)",
                                "rgba(203, 93, 93, 0.8)",
                                "rgba(236, 74, 56, 0.8)",
                                "rgba(255, 0, 0, 0.8)"
        ]

            let x = 50
            for (let i=0; i<brxt_colours.length; i++) {
                svg2.append("rect")
                .attr("x", x)
                .attr("y", 50)
                .attr("width", 20)
                .attr("height",20)
                .style("fill", brxt_colours[i]);

                x = x + 20 
            }
            svg.append("text")
                        .attr("x", 45) // Set the x-coordinate of the text
                        .attr("y", 40) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("Leave"); // Set the text content

            svg.append("text")
                .attr("x", 205) // Set the x-coordinate of the text
                .attr("y", 40) // Set the y-coordinate of the text
                .attr("fill", "black") // Set the fill color of the text
                .attr("font-size", "15px") // Set the font size of the text
                .text("Remain"); // Set the text content

           

        },
        async fetch_brexit_results() {
            fetch('/brexit.json')
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json(); // Parse the JSON data
                })
                .then((data) => {
                    this.brexit_data = data; // Assign the data to geojsonData
                })
                .catch((err) => {
                    this.error = 'Failed to load data: ' + err.message; // Handle errors
                });
        },
        async fetch_imd_data() {
            fetch('/deprivation.json')
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json(); // Parse the JSON data
                })
                .then((data) => {
                    this.deprivation_data = data; // Assign the data to geojsonData
                })
                .catch((err) => {
                    this.error = 'Failed to load data: ' + err.message; // Handle errors
                });
        },
        // async json_test() {
        //     fetch('/uk.geojson')
        //         .then((response) => {
        //             if (!response.ok) {
        //                 throw new Error('Network response was not ok');
        //             }
        //             return response.json(); // Parse the JSON data
        //         })
        //         .then((data) => {
        //             this.geojsonData = data; // Assign the data to geojsonData
        //         })
        //         .catch((err) => {
        //             this.error = 'Failed to load data: ' + err.message; // Handle errors
        //         });
        // },
        // get all ward results in memory
        // apply colour labels to areas conditionally
        // 
        async fetch_ward_results_by_name(ward_name="") {
            fetch(`/election_results.json`)//?ward_name=${ward_name}`)
                .then(response => response.json())
                .then(data => {
                    this.all_ward_election_data = data 

                    if (ward_name !== "") {
                    this.ward_election_datacard = null
                    // console.log(data)
                    const selected_ward_data = data[ward_name]

                    const ward_election_datacard = {}
                    // standard ingo
                    ward_election_datacard['Ward'] = ward_name
                    ward_election_datacard['Previous Election'] = selected_ward_data["Election Date"]
                    // voter behaviour
                    ward_election_datacard['Turnout %'] = selected_ward_data["Voting Summary"]["Turnout"]
                    ward_election_datacard['Electorate'] = selected_ward_data["Voting Summary"]["Electorate"]
                    ward_election_datacard['Votes'] = selected_ward_data["Voting Summary"]["Ballot Papers Issued"]
                    // results
                    ward_election_datacard['Results'] = selected_ward_data['Results'].map((result, index) => {
                        return {
                            [index + 1]: {
                                'Candidate': result['Candidate'],
                                'Party': result['Party'],
                                'Votes': result['Votes'],
                                'Percentage': result['Percentage'],
                                'Outcome': result['Outcome']
                            }
                        };
                    });

                    this.ward_election_datacard = ward_election_datacard
                }

                })

                // .then(data => console.log("Election Results:", data))
                .catch(error => console.error("Error fetching election results:", error));
        },
        async populate_brexit_data(ward_name) {
            this.brexit_election_datacard = null
            let ward_name_formatted = ward_name.replace(/,/g, '')
            ward_name_formatted = ward_name_formatted.replace(/\s+/g, '_')
            const brexit_ward_data = this.brexit_data[ward_name_formatted]
            
            const colour = this.get_brexit_colour(ward_name)

            this.brexit_election_datacard = {}
            this.brexit_election_datacard['leave_percentage'] = brexit_ward_data.leave_percentage
            this.brexit_election_datacard['remain_percentage'] = brexit_ward_data.remain_percentage
            this.brexit_election_datacard['leave_votes'] = brexit_ward_data.leave_votes
            this.brexit_election_datacard['remain_votes'] = brexit_ward_data.remain_votes
            this.brexit_election_datacard['total_votes'] = brexit_ward_data.total_votes
            this.brexit_election_datacard['turnout_percentage'] = brexit_ward_data.turnout_percentage
            this.brexit_election_datacard['electorate'] = brexit_ward_data.electorate
            this.brexit_election_datacard['colour'] = colour
            this.populate_imd_datacard(ward_name)
        },
        populate_imd_datacard(ward_name) {
            this.imd_ward_datacard = null 
            let ward_name_formatted = ward_name.replace(/,/g, '')
            ward_name_formatted = ward_name_formatted.replace(/\s+/g, '_')
            const imd_ward_data = this.deprivation_data[ward_name_formatted]
            this.imd_ward_datacard = {}
            this.imd_ward_datacard['areas'] = imd_ward_data["lsoa_number_of"]
            this.imd_ward_datacard['mean_absolute_deprivation_ranking'] = imd_ward_data["mean_absolute_deprivation_ranking"]
            this.imd_ward_datacard['other_area_info'] = imd_ward_data['lsoa11_ids']
            console.log(this.imd_ward_datacard)
        },
        async initMap() {
            this.title_for_ward_map = 'ward'
            this.reformat_key()

            const ld_colour = 'rgba(250,200,0,0.7)'
            const con_colour = 'rgba(0,0,255,0.7)'
            const lab_colour = 'rgba(250,0,0,0.7)'
            const ind_colour = 'rgba(251, 146, 60, 0.7)'

            const response = await fetch('/election_results.json');
            const election_data = await response.json();
            // Define the projection
            this.projection = d3.geoMercator()
                .center([-2.2580, 51.8341])  
                .scale(255000)                 
                .translate([400, 400]);

            this.path = d3.geoPath().projection(this.projection);

            await d3.json("/gloucester_wards.geojson")
                .then(data => {
                    this.data = data
                    
                    const svg = d3.select(this.$refs.map);

                    //Linear gradient colours need to be set here before implementation
                    svg.append("defs").append("linearGradient")
                    .attr("id", "con_lab")
                    .attr("x1", "0%")
                    .attr("y1", "0%")
                    .attr("x2", "50%")
                    .attr("y2", "0%")
                    .selectAll("stop")
                    .data([
                        { offset: "50%", color: con_colour },
                        { offset: "100%", color: ld_colour}
                    ])
                    .enter().append("stop")
                    .attr("offset", d => d.offset)
                    .attr("stop-color", d => d.color);

                    // Blue-Yellow-Red gradient
                    svg.append("defs").append("linearGradient")
                        .attr("id", "con_ld_lab")
                        .attr("x1", "0%")
                        .attr("y1", "0%")
                        .attr("x2", "100%")
                        .attr("y2", "0%")
                        .selectAll("stop")
                        .data([
                            { offset: "0%", color: con_colour},
                            { offset: "50%", color: ld_colour },
                            { offset: "100%", color: lab_colour }
                        ])
                        .enter().append("stop")
                        .attr("offset", d => d.offset)
                        .attr("stop-color", d => d.color);

                    svg.append("defs").append("linearGradient")
                        .attr("id", "con_indy")
                        .attr("x1", "0%")
                        .attr("y1", "0%")
                        .attr("x2", "55%")
                        .attr("y2", "0%")
                        .selectAll("stop")
                        .data([
                            { offset: "50%", color: con_colour },
                            { offset: "100%", color: ind_colour }
                        ])
                        .enter().append("stop")
                        .attr("offset", d => d.offset)
                        .attr("stop-color", d => d.color);

                    //ADDING A RECTANGLE
                    
                    svg.append("rect")
                        .attr("x", 50)
                        .attr("y", 50)
                        .attr("width", 60)
                        .attr("height",20)
                        .style("fill", con_colour)
                    svg.append("rect")
                        .attr("x", 50)
                        .attr("y", 70)
                        .attr("width", 60)
                        .attr("height",20)
                        .style("fill", ld_colour)
                    svg.append("rect")
                        .attr("x", 50)
                        .attr("y", 90)
                        .attr("width", 60)
                        .attr("height",20)
                        .style("fill", lab_colour)
                    svg.append("rect")
                        .attr("x", 50)
                        .attr("y", 110)
                        .attr("width", 60)
                        .attr("height",20)
                        .style("fill", ind_colour)

                    svg.append("text")
                        .attr("x", 55) // Set the x-coordinate of the text
                        .attr("y", 105) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("LAB"); // Set the text content

                    svg.append("text")
                        .attr("x", 55) // Set the x-coordinate of the text
                        .attr("y", 65) // Set the y-coordinate of the text
                        .attr("fill", "white") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("CON"); // Set the text content

                    svg.append("text")
                        .attr("x", 55) // Set the x-coordinate of the text
                        .attr("y", 85) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("LD"); // Set the text content

                    svg.append("text")
                        .attr("x", 55) // Set the x-coordinate of the text
                        .attr("y", 125) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("IND"); // Set the text content
  
                    // Clear any existing paths
                    svg.selectAll("path").remove();
                    console.log(data)
                    // Draw constituencies

                    function get_colour(d) {
                        if (d.properties.WD24NM === "Churchdown Brookfield with Hucclecote") {
                            return "lightgrey"
                        }
                        //TODO: REPLACE THIS WITH PROGRAMMATIC METHOD
                        //Probably using switch statements to build a string that
                        //can match the id e.g. con_indy
                        if (d.properties.WD24NM === "Barton and Tredworth") {
                            return "url(#con_ld_lab)";  // Return the gradient reference
                        }
                        if (d.properties.WD24NM === "Quedgeley Severn Vale") {
                            return "url(#con_lab)";  // Return the gradient reference
                        }
                        if (d.properties.WD24NM === "Grange") {
                            return "url(#con_indy)";  // Return the gradient reference
                        }
                        if (d.properties.WD24NM === "Tuffley") {
                            return "url(#con_lab)";  // Return the gradient reference
                        }
                        if (d.properties.WD24NM === "Westgate") {
                            return "url(#con_lab)";  // Return the gradient reference
                        }

                        
                        
                        const ward_name = d.properties.WD24NM; // Get the ward name
                        //const color = colorMapping[wardName]; // Match to color mapping
                        //return color ? color : "gray";
                        
                        const ward_seats = election_data[ward_name]['Voting Summary']['Seats']
                        const ward_results = election_data[ward_name]
                        
                        const parties_elected = []
                        for (let i=0;i<ward_seats;i++){
                            parties_elected.push(ward_results.Results[i].Party)                            
                        }
                        
                        //if only one councillor just return colour via switch
                        if (parties_elected.length === 1) {
                            switch(parties_elected[0]) {
                                case 'Labour or Labour & Co-Operative':
                                    return lab_colour;
                                case 'Conservative':
                                    return con_colour;
                                case 'Liberal Democrat':
                                    return ld_colour;
                                case 'Independent':
                                    return ind_colour;
                            }
                        }
                        //if 2 and they are the same
                        if (parties_elected.length === 2) {
                            if (parties_elected[0] === parties_elected[1])
                            switch(parties_elected[0]) {
                                case 'Labour or Labour & Co-Operative':
                                    return lab_colour;
                                case 'Conservative':
                                    return con_colour;
                                case 'Liberal Democrat':
                                    return ld_colour;
                                case 'Independent':
                                    return ind_colour;
                            }
                        }

                        //if 3 and they are the same
                        if (parties_elected.length === 3) {
                            if (parties_elected[0] === parties_elected[1] && parties_elected[1] === parties_elected[2])
                            switch(parties_elected[0]) {
                                case 'Labour or Labour & Co-Operative':
                                    return lab_colour;
                                case 'Conservative':
                                    return con_colour;
                                case 'Liberal Democrat':
                                    return ld_colour;
                                case 'Independent':
                                    return ind_colour;
                            }
                        }
                        //if any slip through default to this
                        return "steelblue"
                    }

                    svg.selectAll("path")
                        .data(data.features)
                        .enter()
                        .append("path")
                        .attr("class", "constituency")
                        .attr("d", this.path)
                        //.style("fill", "steelblue")
                        .style("stroke", "white")
                        .style("stroke-width", 0.5)
                        .on("mouseover", function (event, d) {
                            d3.select(this).style("stroke-width", 2.5);
                            const tooltip = document.getElementById('tooltip');
                            tooltip.style.visibility = 'visible';
                            tooltip.innerHTML = d.properties.WD24NM; // Show ward name
                            tooltip.style.left = event.pageX + 10 + 'px';
                            tooltip.style.top = event.pageY + 10 + 'px';
                        })
                        .on("mouseout", function (event, d) {
                            d3.select(this).style("stroke-width", 0.5);
                            const tooltip = document.getElementById('tooltip');
                            tooltip.style.visibility = 'hidden';
                        })
                        .on("click", (event, d) => {
                            this.selected_json = JSON.stringify(d, null, 2);
                            const data_card = {}
                            data_card["Ward Name"] = d.properties.WD24NM
                            data_card["Ward ID"] = d.properties.FID
                            this.selected_json_datacard = data_card
                            this.fetch_ward_results_by_name(d.properties.WD24NM)
                            this.populate_brexit_data(d.properties.WD24NM)
                            // console.log("Selected Constituency:", d.properties);
                        })
                        .style("fill", d => get_colour(d));
                })
                .catch(error => {
                    console.error("Error loading the GeoJSON:", error);
                });

        },
        async init_poverty_map() {

                            
            const key_elements = Array.from(this.$refs.map.querySelectorAll('rect'));
            key_elements.forEach(element => {
                element.remove()
            })

            const text_elements = Array.from(this.$refs.map.querySelectorAll('text'));
            text_elements.forEach(element => {
                element.remove()
            })
                    // key_elements[0].style = "fill: rgba(59, 145, 204, 0.9)"
                    // key_elements[1].style = "fill: rgba(40, 109, 156, 0.5)"
                    // key_elements[2].style = "fill: rgba(18, 77, 117, 0.3)"
                    // key_elements[3].style = "fill: rgba(19, 59, 87, 0.1)"

            this.title_for_ward_map = 'deprivation' 
            const imd_colours = ["rgba(255,51,51,1)",
                                "rgba(255,71,71,0.8)",
                                "rgba(237,146,90,0.8)",
                                "rgba(251,181,103,0.7)",
                                "rgba(233,209,99,0.6)",
                                "rgba(235,224,124,0.6)",
                                "rgba(200,231,86,0.6)",
                                "rgba(146,186,80,0.7)",
                                "rgba(105,171,87,0.8)",
                                "rgba(47,160,43,0.8)"]

            const response = await fetch('/deprivation.json');
            const poverty_data = await response.json();
            console.log(poverty_data)
            // Define the projection
            this.projection = d3.geoMercator()
                .center([-2.2580, 51.8341])  
                .scale(255000)                 
                .translate([400, 400]);

            this.path = d3.geoPath().projection(this.projection);

            await d3.json("/gloucester_wards.geojson")
                .then(data => {
                    this.data = data
                    
                    const svg = d3.select(this.$refs.map);
                    
                    // add key
                    let x = 50
                    for (let i=0; i<9; i++) {
                        svg.append("rect")
                        .attr("x", x)
                        .attr("y", 50)
                        .attr("width", 20)
                        .attr("height",20)
                        .style("fill", imd_colours[i]);

                        x = x + 20 
                    }

                    svg.append("text")
                        .attr("x", 25) // Set the x-coordinate of the text
                        .attr("y", 40) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("Most Deprived"); // Set the text content

                    svg.append("text")
                        .attr("x", 165) // Set the x-coordinate of the text
                        .attr("y", 40) // Set the y-coordinate of the text
                        .attr("fill", "black") // Set the fill color of the text
                        .attr("font-size", "15px") // Set the font size of the text
                        .text("Least Deprived"); // Set the text content
                    

                    // Clear any existing paths
                    svg.selectAll("path").remove();
                  
                    // Draw constituencies

                    function get_colour(d) {
                        
                        let ward_name_formatted = d.properties.WD24NM.replace(/,/g, '')
                        ward_name_formatted = ward_name_formatted.replace(/\s+/g, '_')
                        const ward_poverty_data = poverty_data[ward_name_formatted]
                        
                        if (ward_poverty_data) {
                        
                        
                        const mean_absolute_dep_ranking = poverty_data[ward_name_formatted]['mean_absolute_deprivation_ranking']
                        //let range_category = Math.floor(mean_absolute_dep_ranking); // Round to nearest integer

                        switch (true) {
                            case (mean_absolute_dep_ranking >= 0 && mean_absolute_dep_ranking < 10):
                                return imd_colours[0];  
                            case (mean_absolute_dep_ranking >= 10 && mean_absolute_dep_ranking < 20):
                                return imd_colours[1];  
                            case (mean_absolute_dep_ranking >= 20 && mean_absolute_dep_ranking < 30):
                                return imd_colours[2];  
                            case (mean_absolute_dep_ranking >= 30 && mean_absolute_dep_ranking < 40):
                                return imd_colours[3];  
                            case (mean_absolute_dep_ranking >= 40 && mean_absolute_dep_ranking < 50):
                                return imd_colours[4];  
                            case (mean_absolute_dep_ranking >= 50 && mean_absolute_dep_ranking < 60):
                                return imd_colours[5];  
                            case (mean_absolute_dep_ranking >= 60 && mean_absolute_dep_ranking < 70):
                                return imd_colours[6];  
                            case (mean_absolute_dep_ranking >= 70 && mean_absolute_dep_ranking < 80):
                                return imd_colours[7];  
                            case (mean_absolute_dep_ranking >= 80 && mean_absolute_dep_ranking < 90):
                                return imd_colours[8];  
                                case (mean_absolute_dep_ranking >= 90 && mean_absolute_dep_ranking < 100):
                                    return imd_colours[9];   
                                default:
                                    return 'steelblue';  // Default color if out of the range
                            }
                                } else {
                                    return "steelblue"
                                }
                    }

                            svg.selectAll("path")
                                .data(data.features)
                                .enter()
                                .append("path")
                                .attr("class", "constituency")
                                .attr("d", this.path)
                                //.style("fill", "steelblue")
                                .style("stroke", "white")
                                .style("stroke-width", 0.5)
                                .on("mouseover", function (event, d) {
                                    d3.select(this).style("stroke-width", 2.5);
                                    const tooltip = document.getElementById('tooltip');
                                    tooltip.style.visibility = 'visible';
                                    tooltip.innerHTML = d.properties.WD24NM; // Show ward name
                                    tooltip.style.left = event.pageX + 10 + 'px';
                                    tooltip.style.top = event.pageY + 10 + 'px';
                                })
                                .on("mouseout", function (event, d) {
                                    d3.select(this).style("stroke-width", 0.5);
                                    const tooltip = document.getElementById('tooltip');
                                    tooltip.style.visibility = 'hidden';
                                })
                                .on("click", (event, d) => {
                                    this.selected_json = JSON.stringify(d, null, 2);
                                    const data_card = {}
                                    data_card["Ward Name"] = d.properties.WD24NM
                                    data_card["Ward ID"] = d.properties.FID
                                    this.selected_json_datacard = data_card
                                    this.fetch_ward_results_by_name(d.properties.WD24NM)
                                    this.populate_brexit_data(d.properties.WD24NM)
                                    // console.log("Selected Constituency:", d.properties);
                                })
                                .style("fill", d => get_colour(d));
                        })
                        .catch(error => {
                            console.error("Error loading the GeoJSON:", error);
                        });
                }
            }
        }
</script>

<style>
.country {
    transition: fill 0.3s;
}

/* Add these new stripe patterns */
/* .striped-blue-yellow {
    background: repeating-linear-gradient(
        45deg,
        rgba(37, 99, 235,0.5), 
        rgba(37, 99, 235,0.5) 10px,
        rgba(250, 204, 21, 0.5) 10px,
        rgba(250, 204, 21) 20px,
        rgba(255, 233, 233, 0.5) 10px,
        rgb(250, 21, 21) 20px
    );
} */

.striped-blue-yellow {
    background: repeating-linear-gradient(
        45deg,
        rgba(37, 99, 235, 0.5) 0px,
        rgba(37, 99, 235, 0.5) 10px,
        rgba(240, 240, 240, 0.5) 10px,
        rgba(253, 253, 253, 0.5) 20px,
        rgba(239, 68, 68, 0.5) 20px,
        rgba(239, 68, 68, 0.5) 30px
    );
}
</style>