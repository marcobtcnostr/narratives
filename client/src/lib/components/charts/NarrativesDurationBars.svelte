<!-- src\lib\components\charts\NarrativesDurationBars.svelte -->
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
			
			// Now inside onMount, we check if it's the browser environment
			drawChart();

			// Set up the ResizeObserver to listen for size changes
			resizeObserver = new ResizeObserver((entries) => {
				updateDimensions();
				drawChart();
			});

			// Start observing the chart container
			resizeObserver.observe(chartContainer);

			// Listen for window resize events as well
			window.addEventListener('resize', drawChart);
		}
	});

	onDestroy(() => {
		if (browser && resizeObserver) {
			// Disconnect the ResizeObserver
			resizeObserver.unobserve(chartContainer);
			// Remove the resize event listener
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

		// Clear any existing SVG
		d3.select(chartContainer).selectAll('*').remove();

		// Aggregate duration by publisher
		const durationByPublisher = d3.rollup(
			data.map((d) => ({ ...d, publisher: d.publisher || 'Unknown' })), // Replace null publisher with 'Unknown',
			(v) => d3.sum(v, (d) => d.duration),
			(d) => d.publisher
		);

		const dataArray = Array.from(durationByPublisher, ([publisher, duration]) => ({
			publisher,
			duration
		})).sort((a, b) => b.duration - a.duration); // Sort by duration

		updateDimensions(); // Update the dimensions every time you draw the chart

		// Append the svg object to the chart container
		const svg = d3
			.select(chartContainer)
			.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		// Create a color scale using D3's schemeCategory10 or define your own range of colors
		const colorScale = d3
			.scaleOrdinal()
			.domain(dataArray.map((d) => d.publisher)) // Use the unique publishers as the domain
			.range(d3.schemeCategory10); // This is an array of 10 categorical colors

		// Y axis
		const maxYValue = Math.max(
			d3.max(dataArray, (d) => d.duration),
			60
		); // Ensure minimum of 60
		const adjustedMaxYValue = Math.ceil(maxYValue / 60) * 60; // Round up to nearest 60
		const y = d3.scaleLinear().domain([0, adjustedMaxYValue]).range([height, 0]);
		svg.append('g').call(d3.axisLeft(y).tickValues(d3.range(0, adjustedMaxYValue + 1, 15))); // Ticks every 15 minutes

		// X axis
		const x = d3
			.scaleBand()
			.range([0, width])
			.domain(dataArray.map((d) => d.publisher))
			.padding(0.1);
		svg
			.append('g')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x))
			.selectAll('text')
			.style('text-anchor', 'end')
			.attr('transform', 'rotate(-45)'); // Rotate the text for better readability

		// Adding a label for the Y axis to indicate it's in minutes
		svg
			.append('text')
			.attr('text-anchor', 'end')
			.attr('transform', 'rotate(-90)') // Rotate the text for a vertical label
			.attr('y', -margin.left + 22) // Adjust the position based on your margin
			.attr('x', 0 - height / 2)
			.text('(min)') // Text label for the Y axis
			.style('fill', 'var(--text-color)'); // Use CSS variable for text color

		// Bars
		svg
			.selectAll('myRect')
			.data(dataArray)
			.join('rect')
			.attr('x', (d) => x(d.publisher))
			.attr('y', (d) => y(d.duration))
			.attr('width', x.bandwidth())
			.attr('height', (d) => height - y(d.duration))
			.attr('fill', (d) => (d.publisher === 'Unknown' ? '#aaa' : colorScale(d.publisher))); // Conditional fill color
	}
</script>

<div bind:this={chartContainer} id="duration-bar-chart" style="width: 100%; height: 100%;"></div>
