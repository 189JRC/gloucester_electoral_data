<template>
    <div class="flex flex-row">
        <div id="council-election-results" class="flex-1">
            <!--TODO: Conditional render of colour from party selected_constituency['winning_party']-->
            <div class="text-center border border-gray-700 text-xl py-4">
                <strong class="text-4xl">July 2024 Election</strong>
            </div>
            <div
                class="bg-blue-500 mt-5 text-2xl text-center border-l border-b border-t border-r border-gray-700 text-xl py-2">
                <p>Constituency: <strong>{{ selected_constituency.constituency_name }}</strong></p>
                <p>Region: <strong>{{ selected_constituency.region }}</strong></p>
                MP: <strong>{{ selected_constituency.candidates[0].full_name }}</strong><br>
                <!-- <p>Designation: <strong> {{ selected_constituency.const_designation }}</strong></p> -->
            </div>
            <div class="text-2xl border-l border-r border-b border-gray-700 pl-3 pr-3 py-2">
                Result: <strong>{{ selected_constituency.result_summary }}</strong>
                <br>
                Electorate: <strong>{{ selected_constituency.electorate }}</strong><br>
                Turnout: <strong>{{ selected_constituency.votes_counted }} / {{ (selected_constituency.votes_counted /
                    selected_constituency.electorate *
                    100).toFixed(2) }}%</strong><br>
                Majority: <strong>{{ selected_constituency.majority }} votes / {{
                    (selected_constituency.majority_pct_votes).toFixed(2)
                }}%</strong><br>

                <!-- {{  selected_constituency }} -->
            </div>
            <div>
            </div>

        </div>

    </div>
    <div class="mt-5 flex items-center">
        <label for="toggle" class="flex items-center cursor-pointer">
            <!-- Toggle Container -->
            <div class="relative">
                <!-- Input -->
                <input @click="toggle_slider" type="checkbox" id="toggle" class="sr-only">
                <!-- Slider -->
                <div class="block bg-gray-600 w-20 h-8 rounded-full"></div>
                <!-- Circle -->
                <div class="dot absolute left-1 top-1 bg-white w-10 h-6 rounded-full transition"></div>
            </div>
            <!-- Label Text -->
        </label>
    </div>
    <div class='text-2xl border border-gray-700 mt-5 pl-3 pr-3 py-2'>
        <!-- <div class='text-2xl border border-gray-700 mt-5 pl-3 pr-3 py-2'> -->
        <strong>Marginal Seats Scale </strong>
        <br>
        <div>
            <!-- <input type="checkbox" @click="allow_marginal_seats_slider" class="form-checkbox w-6 h-6"> -->

            Show seats with margin less than: <strong>{{ marginals_threshold }}</strong>
            <div class="flex items-center space-x-4">
                <input type="range" v-model="marginals_threshold" @input="marginal_seats_threshold" min="18" max="21500"
                    class="mt-3 w-full h-7 bg-gray-100 border border-gray-500 rounded-lg appearance-none cursor-pointer" />
                <div></div>
            </div>
        </div>
    </div>
    <div class='text-2xl border border-gray-700 mt-5 pl-3 pr-3 py-2'>
        <!-- <div class='text-2xl border border-gray-700 mt-5 pl-3 pr-3 py-2'> -->
        <!-- {{ election_turnout_slider }} -->


        <!-- <input type="checkbox" @click="allow_turnout_slider" class="form-checkbox w-6 h-6"> -->

        <strong>Election Turnout Scale </strong>{{ seat_count }}
        <br>



        Turnout greater than: <strong>{{ turnout_threshold }}%</strong>
        <div class="flex items-center space-x-4">
            <input type="range" v-model="turnout_threshold" @input="change_turnout_threshold" min="30" max="75"
                class="mt-3 w-full h-7 bg-gray-100 border border-gray-500 rounded-lg appearance-none cursor-pointer" />
            <div></div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        selected_constituency: {
            type: Object,
            required: true
        },
        seat_count: {
            type: Object,
            required: false
        },
        

    },
    emits: ['update-seat-threshold', 'turnout-threshold-changed'],
    data() {
        return {
            //Constituency datacard child component
            marginals_threshold: 5000,
            colour_setting: "Neutral",
            turnout_threshold: 50,
            marginal_seats_slider: true,
            election_turnout_slider: false
        }
    },
    methods: {
        toggle_slider() {
            if (this.marginal_seats_slider = true) {
                this.marginal_seats_slider = false; this.election_turnout_slider = true
                console.log("marginal_seats_slider", this.marginal_seats_slider)
                console.log("election_turnout_slider", this.election_turnout_slider)

            } else {
                console.log("marginal_seats_slider", this.marginal_seats_slider)
                console.log("election_turnout_slider", this.election_turnout_slider)
                this.marginal_seats_slider = null; this.election_turnout_slider = false
            }
        },
        marginal_seats_threshold() {
            this.$emit('update-seat-threshold', this.marginals_threshold);
        },
        change_turnout_threshold() {
            this.$emit('turnout-threshold-changed', this.turnout_threshold);
        },
        change_colour_setting() {
            //this.colour_setting = this.colour_setting === 'Neutral' ? 'Colours' : this.colour_setting;
            //this.colour_setting = this.colour_setting === 'Colours' ? 'Neutral' : this.colour_setting;
            if (this.colour_setting === 'Neutral') {
                this.colour_setting = 'Colours'
                this.$emit('selected-colours-changed', this.colour_setting);
            } else {
                this.colour_setting = 'Neutral'
                this.$emit('selected-colours-changed', this.colour_setting);
            }
        }
    }
}
</script>
<style>
input[type="range"]::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #7bc27b;
    border-radius: 50%;
    cursor: pointer;
}

input:checked~.dot {
    transform: translateX(77%);
}
</style>