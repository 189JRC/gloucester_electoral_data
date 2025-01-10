<script setup>
import MapComponent from './components/MapComponent.vue'
import ExperimentalComponent from './components/ExperimentalComponent.vue'
</script>

<template>
  <div class="pt-5 pl-5">
    <button @click="reset" class="p-2 bg-blue-100 border-2 border-black mx-2 text-xl ">Home</button>
    <div class="mt-5" v-if="show_buttons">
      <button @click="render_councils" class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl ">Council Maps</button>
      <button @click="render_constituencies" class="p-2 bg-gray-100 border-2 border-black mx-2 text-xl ">National Constituency Map</button>
    </div>
  </div>
  <div v-if="show_councils">
    <MapComponent/>
  </div>
  <div v-if="show_constituencies">
    <ExperimentalComponent/>
  </div>
  
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
  data() {
    return {
      show_constituencies: false,
      show_councils: false,
      show_buttons: true
    };
  },
  mounted() {
  },
  methods: {
    reset() {
      this.show_buttons = true
      this.show_constituencies = false
      this.show_councils = false
    },
    render_constituencies() {
      this.show_constituencies = true
      this.show_councils = false
    },
    render_councils() {
      this.show_councils = true
      this.show_constituencies = false
    }
  },
}
</script>
