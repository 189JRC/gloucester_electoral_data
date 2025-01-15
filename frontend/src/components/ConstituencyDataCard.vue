<template>
    <div class="flex flex-row">
        <div id="column-2" class="text-3xl flex-1">
            <strong>CANDIDATES:</strong>
            <!-- <table>
                    <th class="px-10">Name: </th>
                    <th class="pl-10">Hi2</th>
                    <th class="pl-10">Hi2</th>
                    </table> -->
                    <div class="overflow-auto max-h-1/2" style="height: 70vh;">
            <div v-for="(candidate, index) in selected_constituency.candidates" :key="index" class="text-2xl border border-gray-700 pl-3 pr-3 py-1 mb-2">
               

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
                
            </div>
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
    },
    data() {
        return {
            //Constituency datacard child component
            colour_setting: "Neutral"
        }
    },
    methods: {
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