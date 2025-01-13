<template>
    <div class="flex flex-row">

        <div id="council-election-results" class="flex-1">
            <p>Constituency: <strong>{{ selected_constituency.constituency_name }}</strong></p>
            <p>Region: <strong>{{ selected_constituency.region }}</strong></p>
            <p>Designation: <strong> {{ selected_constituency.const_designation }}</strong></p>
            <div class="mt-5 text-center border-l border-b border-t border-gray-700 text-xl py-2">
                July 2024 Election Information
            </div>

            <div class="border-l border-gray-700 pl-3 py-2">
                Result: <strong>{{ selected_constituency.result_summary }}</strong>
                <br>
                Electorate: <strong>{{ selected_constituency.electorate }}</strong><br>
                Votes Counted: <strong>{{ selected_constituency.votes_counted }}</strong><br>
                Turnout: <strong>{{ (selected_constituency.votes_counted / selected_constituency.electorate *
                    100).toFixed(2) }}%</strong><br>
                Majority: <strong>{{ selected_constituency.majority }}</strong><br>
                Majority as % of total votes cast: <strong>{{ (selected_constituency.majority_pct_votes).toFixed(2)
                    }}%</strong><br>
                MP: <strong>{{ selected_constituency.candidates[0].full_name }}</strong><br>
                <!-- {{  selected_constituency }} -->
                <br>
                <strong>Seat Count: </strong>{{ seat_count }}
                <br>
                <div v-if="show_margin_scale">
                    MARGIN scale
                    <div class="flex items-center space-x-4">
                        <input type="range" v-model="user_selected_margin" @input="updateValue" min="18" max="21500"
                            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" />
                        <div>{{ user_selected_margin }}</div>
                    </div>
                </div>
            </div>
            <hr class="border-t-3 border-gray-500">

            <div>

                <!-- <div v-if="election_datacard" class="text-center border-l border-b border-gray-700 text-xl">
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

                        </div> -->
            </div>
        </div>
        <div id="column-2" class="flex-1">
            <strong>CANDIDATES:</strong>
            <div v-for="(candidate, index) in selected_constituency.candidates" :key="index" class="candidate-card">
                <h3>Position: {{ candidate.rank }}</h3>
                <p>Name: {{ candidate.full_name }}</p>
                <p>Party: {{ candidate.party }}</p>
                <p>Vote Count: {{ candidate.vote_count }}</p>
                <p>Vote Share: {{ (candidate.vote_share * 100).toFixed(2) }}%</p>
                <p>Votes needed to win: {{ candidate.votes_to_win }}</p>
                <!-- <p>Sitting MP: {{ candidate.sitting_mp }}</p>
      <p>Former MP: {{ candidate.former_mp }}</p>
      //will error if rounded as some are null!!
      <p>Vote Change: {{ candidate.vote_change }}%</p> -->
                <!-- {{ candidate }} -->
                <hr>
            </div>

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
        show_margin_scale: {
            type: Boolean,
            required: false
        },
    },
    data() {
        return {
            //Constituency datacard child component
            user_selected_margin: 5000,
        }
    },
    methods: {
        updateValue(event) {
            this.user_selected_margin = event.target.value;
            this.$emit('selected-margin-changed', this.user_selected_margin); 
        },
    }
}
</script>
<style>
/* Optional custom styles for the slider thumb */
input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    background: #4F46E5;
    /* Tailwind's indigo-500 color */
    border-radius: 50%;
    cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #4F46E5;
    border-radius: 50%;
    cursor: pointer;
}
</style>