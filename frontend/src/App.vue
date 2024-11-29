<script setup>
import MapComponent from './components/MapComponent.vue'
import MapSelection from './components/MapSelection.vue'
import MapSelectionRefactored from './components/MapSelectionRefactored.vue';
import ExperimentalComponent from './components/ExperimentalComponent.vue'
</script>

<template>

  <MapSelection @update-map="handleValueChange" />
  <MapComponent v-if="selected_map === 'Gloucester'" />
  <MapSelectionRefactored v-if="selected_map === 'Oldham West'"/>
  <!-- <ExperimentalComponent /> -->
  <!-- <div class="mt-5 p-6 max-w-sm mx-auto dark:bg-gray-800 rounded-xl shadow-md flex items-center space-x-4">
    <div class="flex-shrink-0">
      <img class="h-12 w-12" src="/vite.svg" alt="ChitChat Logo">
    </div>
    <div>
      <div class="text-xl font-medium dark:text-white">ChitChat</div>
      <p class="dark:text-gray-300">You have a new message!</p>
    </div>
  </div>

  <div
    class="mt-5 p-6 max-w-sm mx-auto dark:bg-gray-700 rounded-xl shadow-md flex justify-between items-center space-x-4">
    <div>
      <div class="text-xl font-medium dark:text-white">ChitChat</div>
      <p class="dark:text-gray-300">You have a new message!</p>
    </div>
    <div class="flex-shrink-0">
      <img class="h-12 w-12" src="./assets/vue.svg" alt="ChitChat Logo">
    </div>
  </div>



  <div
    class="mt-5 p-6 max-w-sm mx-auto dark:bg-gray-600 rounded-xl shadow-md ">
  <HelloWorld msg="Website Scaffolding" />
  </div> -->
</template>

<script>

export default {
  name: "DropdownSelect",
  props: {
  },
  data() {
    return {
      selected_map: 'Gloucester'
    };
  },
  computed: {
    selected() {
      return this.modelValue;
    },
  },
  methods: {
    handleValueChange(selected_map) {
      console.log("Selected value:", selected_map);
      this.selected_map = selected_map
    },
  },
}

</script>
