<template>
    <div class="relative w-64" @click="toggleDropdown">
        <div
            class="px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500">
            Map Choice
        </div>
        <ul v-if="isOpen"
            class="absolute left-0 right-0 z-10 mt-2 bg-white border border-gray-300 rounded-md shadow-lg max-h-48 overflow-y-auto">
            <li @click="selectOption(option)" v-for="option in options" :key="option" >
                {{ option }}
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "DropdownSelect",
    props: {
    },
    data() {
        return {
            options: ['Gloucester', 'Oldham West'],
            isOpen: false,
        };
    },
    computed: {
        selected() {
            return this.modelValue;
        },
    },
    methods: {
        toggleDropdown() {
            this.isOpen = !this.isOpen;
        },
        selectOption(option) {
            console.log(option)
            this.$emit("update-map", option);
        },
    },
};
</script>