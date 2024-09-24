<!-- src\lib\components\charts\NarrativesWorldMap.svelte -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3';
	import { browser } from '$app/environment'; // Import the browser check
	import { narrativesStore } from '$lib/stores/narratives-stores';
	import WorldMap from '$lib/json/WorldMap.json'; // Adjust path as necessary

	let chartContainer: HTMLElement;
	let resizeObserver;
	let rotation = [0, 0, 0]; // Initial rotation for the globe
	let velocity = [0.01, -0.005, 0]; // Initial velocity for the rotation

	// $: data = $narrativesStore; 
	let width, height;

	export let dataStore; // Accept the store
	let data = [];

	onMount(() => {
		if (browser) {

			// Reactively update the chart when the store changes
			dataStore.subscribe((value) => {
				data = value;
				drawMap();
			});
			
			// Check if it's running in the browser
			drawMap();

			// Set up the ResizeObserver to listen for size changes
			resizeObserver = new ResizeObserver((entries) => {
				drawMap();
			});

			// Start observing the chart container
			resizeObserver.observe(chartContainer);

			// Listen for window resize events as well
			window.addEventListener('resize', drawMap);
		}
	});

	onDestroy(() => {
		if (browser && resizeObserver) {
			// If it's the browser and resizeObserver was created, clean up
			resizeObserver.unobserve(chartContainer);
			window.removeEventListener('resize', drawMap);
		}
	});

	$: if ($narrativesStore) {
		drawMap();
	}

	function drawMap() {
		if (!chartContainer || !data) return;

		// Clear previous contents
		d3.select(chartContainer).selectAll('*').remove();

		// Set up dimensions based on container size
		width = chartContainer.clientWidth;
		height = chartContainer.clientHeight;

		// Create SVG element
		const svg = d3.select(chartContainer).append('svg').attr('width', width).attr('height', height);

		// Define projection and path
		const projection = d3.geoOrthographic().fitSize([width, height], WorldMap);
		const path = d3.geoPath().projection(projection);

		// Compute total duration by country
		const durationByCountry = d3.rollup(
			data,
			(v) => d3.sum(v, (d) => d.duration),
			(d) => d.country
		);

		// Collect all country names for the ordinal color scale domain
		const countries = Array.from(new Set(data.map((d) => d.country)));

		// Create an ordinal color scale using the country names
		const colorScale = d3.scaleOrdinal().domain(countries).range(d3.schemeCategory10);

		// Draw countries
		svg
			.selectAll('path')
			.data(WorldMap.features)
			.enter()
			.append('path')
			.attr('d', path)
			.attr('fill', (d) => {
				const country = d.properties.sovereignt;
				const duration = durationByCountry.get(country) || 0;
				return duration < 1 ? 'var(--text-color)' : colorScale(country);
			});

		// Improved dragging function
		function dragstarted(event) {
			d3.select(this).style('cursor', 'grabbing');
		}

		function dragged(event) {
			// Update the globe's rotation
			const rotate = projection.rotate();
			const k = sensitivity / projection.scale();
			rotation = [rotate[0] + event.dx * k, rotate[1] - event.dy * k];
			projection.rotate(rotation);
			svg.selectAll('path').attr('d', path);
		}

		function dragended(event) {
			d3.select(this).style('cursor', 'grab');
		}

		const sensitivity = 50;

		// Apply dragging to the SVG
		svg.call(d3.drag().on('start', dragstarted).on('drag', dragged).on('end', dragended));
	}
</script>

<div bind:this={chartContainer} style="width: 100%; height: 100%;"></div>
