<template>
    <div class="flex mt-5">

        <div class="flex-1 h-1/2 w-1/3 px-5 mx-auto">
            <div class="border-4 border-gray-700 text-xl p-5 text-center">
            </div>
            <div class="border-2 border-gray-300 bg-gray-50 mt-5">
                <svg ref="map" width="1000" height="600"></svg>
            </div>
            <div id="tooltip"
                style="position: absolute; visibility: hidden; background: white; padding: 5px; border: 1px solid black;">
            </div>
            <div class="flex justify-center mt-2 border-gray-500">
                <button class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl ">button</button>
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
                        <div class="text-center border-l border-b border-gray-700 text-xl"><strong>Results</strong><br>
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
            res: null,
            projection: null
        };
    },
    mounted() {
        this.init()
    },
    methods: {
        async init() {
        try {
            await this.init_constituency_map();  // Pass the result to the map function after it's loaded
        } catch (error) {
            console.error('Error loading election results or initializing map:', error);
        }
    },
        async init_constituency_map() {
    
            // Define the projection
            this.projection = d3.geoMercator()
                .center([0.06225, -0.06935])
                .scale(325000)
                .translate([400, 400]);

            this.path = d3.geoPath().projection(this.projection);

            await d3.json("/constituencies_2024.geojson")
                .then()
                .then(data => {
                    const svg = d3.select(this.$refs.map);
                    // Clear any existing paths
                    svg.selectAll("path").remove();
                    
                    // Draw constituencies

                    function apply_party_colour(d) {
                        return "pink"
                }

                    svg.selectAll("path")
                        .data(data.features)
                        .enter()
                        .append("path")
                        .attr("class", "constituency")
                        .attr("d", this.path)
                        .style("fill", "gray")
                        .style("stroke", "white")
                        .style("stroke-width", 0.5)
                        .on("mouseover", function (event, d) {
                            d3.select(this).style("stroke-width", 2.5);
                            const tooltip = document.getElementById('tooltip');
                            tooltip.style.visibility = 'visible';
                            tooltip.innerHTML = d.properties.n; // Show ward name
                            tooltip.style.left = event.pageX + 10 + 'px';
                            tooltip.style.top = event.pageY + 10 + 'px';
                        })
                        .style("fill", d => apply_party_colour(d));
                })
                .catch(error => {
                    console.error("Error loading the GeoJSON:", error);
                });

        },
    }
}
</script>