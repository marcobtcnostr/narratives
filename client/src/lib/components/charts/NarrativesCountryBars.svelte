<!-- src\lib\components\charts\NarrativesCountryBars.svelte -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as d3 from 'd3';
	import { browser } from '$app/environment';
	import { narrativesStore } from '$lib/stores/narratives-stores';

	// $: data = $narrativesStore;
	let chartContainer: HTMLElement;
	let resizeObserver;

	export let dataStore; // Accept the store
	let data = [];

	onMount(() => {
		if (browser) {

			// Reactively update the chart when the store changes
			dataStore.subscribe((value) => {
				data = value;
				drawChart();
			});
			
			drawChart();
			resizeObserver = new ResizeObserver((entries) => {
				updateDimensions();
				drawChart();
			});
			resizeObserver.observe(chartContainer);
			window.addEventListener('resize', drawChart);
		}
	});

	onDestroy(() => {
		if (browser && resizeObserver) {
			resizeObserver.unobserve(chartContainer);
			window.removeEventListener('resize', drawChart);
		}
	});

	$: if ($narrativesStore) {
		drawChart();
	}

	let width, height;
	const margin = { top: 20, right: 30, bottom: 50, left: 50 };

	function updateDimensions() {
		width = chartContainer.clientWidth - margin.left - margin.right;
		height = chartContainer.clientHeight - margin.top - margin.bottom;
	}

	function drawChart() {
		if (!chartContainer || !data) return;

		d3.select(chartContainer).selectAll('*').remove();

		// Aggregate duration by country
		const durationByCountry = d3.rollup(
			data.map((d) => ({ ...d, country: d.country || 'Unknown' })), // Replace null country with 'Unknown',,
			(v) => d3.sum(v, (d) => d.duration),
			(d) => d.country
		);

		const totalDuration = d3.sum(Array.from(durationByCountry.values()));

		// Convert the Map to an Array of objects with percentage
		// const dataArray = Array.from(durationByCountry, ([country, duration]) => ({
		// 	country,
		// 	percentage: (duration / totalDuration) * 100
		// })).sort((a, b) => b.percentage - a.percentage);

		const dataArray = Array.from(durationByCountry, ([country, duration]) => ({
			country,
			percentage: (duration / totalDuration) * 100
		}));

		updateDimensions(); // Update the dimensions every time you draw the chart

		const svg = d3
			.select(chartContainer)
			.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		// Update color scale if needed
		const colorScale = d3
			.scaleOrdinal()
			.domain(dataArray.map((d) => d.country))
			.range(d3.schemeCategory10);

		// Y axis for percentage
		const y = d3
			.scaleLinear()
			.domain([0, d3.max(dataArray, (d) => d.percentage) || 100])
			.range([height, 0]);
		svg.append('g').call(d3.axisLeft(y));

		// X axis for countries
		const x = d3
			.scaleBand()
			.range([0, width])
			.domain(dataArray.map((d) => d.country))
			.padding(0.1);
		svg
			.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x))
			.selectAll('text')
			.style('text-anchor', 'end')
			.attr('transform', 'rotate(-45)');

		// Adding a label for the Y axis to indicate it's in minutes
		svg
			.append('text')
			.attr('text-anchor', 'end')
			.attr('transform', 'rotate(-90)') // Rotate the text for a vertical label
			.attr('y', -margin.left + 22) // Adjust the position based on your margin
			.attr('x', 0 - height / 2)
			.text('(%)') // Text label for the Y axis
			.style('fill', 'var(--text-color)'); // Use CSS variable for text color

		// Bars for percentage
		svg
			.selectAll('myRect')
			.data(dataArray)
			.join('rect')
			.attr('x', (d) => x(d.country))
			.attr('y', (d) => y(d.percentage))
			.attr('width', x.bandwidth())
			.attr('height', (d) => height - y(d.percentage))
			.attr('fill', (d) => (d.country === 'Unknown' ? '#aaa' : colorScale(d.country))); // Conditional fill color
	}
</script>

<div bind:this={chartContainer} id="country-bar-chart" style="width: 100%; height: 100%;"></div>
