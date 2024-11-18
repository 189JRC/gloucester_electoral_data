<template>
    <div ref="sphereContainer"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
    name: 'SphericalObject',
    props: {
        smallSpheres: [
                    { size: 20, color: "red", position: [50, 0, 0] },
                    { size: 30, color: "green", position: [-50, 0, 0] },
                    { size: 15, color: "blue", position: [0, 50, 0] },
                    // Add more spheres as needed
                ],
    },
    mounted() {
        this.createSphere({ size: 200, color: "red", position: [50, 0, 0] });
        this.createSphere({ size: 300, color: "green", position: [-50, 0, 0] });
        this.createSphere({ size: 150, color: "blue", position: [0, 50, 0] });
    },
    methods: {
        createSphere(sphereData) {
            const width = sphereData.size * 2;
            const height = sphereData.size * 2;

            const projection = d3.geoOrthographic()
                .scale(sphereData.size) // Scale by the radius prop
                .translate([width / 2, height / 2]);

            const path = d3.geoPath().projection(projection);

            const svg = d3.select(this.$refs.sphereContainer)
                .append('svg')
                .attr('width', width)
                .attr('height', height);

            svg.append('path')
                .datum({ type: 'Sphere' })
                .attr('d', path)
                .attr('fill', sphereData.color)
                .attr('stroke', '#333');
        }
    }
};
</script>

<style scoped>
div {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>