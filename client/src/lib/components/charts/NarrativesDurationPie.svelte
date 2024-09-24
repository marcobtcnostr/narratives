<!-- src\lib\components\charts\NarrativesDurationPie.svelte -->
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

	function drawChart() {
		if (!chartContainer || !data) return;

		d3.select(chartContainer).selectAll('*').remove();

		const width = chartContainer.clientWidth;
		const height = chartContainer.clientWidth;
		const radius = Math.min(width, height) / 3.25; // Adjust the radius as needed

		// Aggregate duration by publisher
		const durationByPublisher = d3.rollup(
			data.map((d) => ({ ...d, publisher: d.publisher || 'Unknown' })),
			(v) => d3.sum(v, (d) => d.duration),
			(d) => d.publisher
		);

		const dataArray = Array.from(durationByPublisher, ([publisher, duration]) => ({
			publisher,
			duration
		})).sort((a, b) => b.duration - a.duration); // Sort by duration

		const totalDuration = d3.sum(dataArray, (d) => d.duration);

		const pie = d3
			.pie()
			.sort(null)
			.value((d) => d.duration);

		// Adjust the innerRadius here to create the donut shape
		const arc = d3
			.arc()
			.innerRadius(radius * 0.75) // Make the donut hole by setting a nonzero innerRadius
			.outerRadius(radius);

		const color = d3.scaleOrdinal(d3.schemeCategory10);

		const labelArc = d3
			.arc()
			.outerRadius(radius * 1.25)
			.innerRadius(radius * 1.5); // Label arc has the same outer and inner radius for placing text on the edge

		const svg = d3
			.select(chartContainer)
			.append('svg')
			.attr('width', width)
			.attr('height', height)
			.append('g')
			.attr('transform', `translate(${width / 2},${height / 2})`);

		svg
			.selectAll('.arc')
			.data(pie(dataArray))
			.enter()
			.append('g')
			.attr('class', 'arc')
			.append('path')
			.attr('d', arc)
			.attr('fill', (d) => color(d.data.publisher))
			.each(function (d, i) {
				// Save the initial angles
				this._current = d;
			});

		// Place percentage text just outside the slices
		svg
			.selectAll('.arc')
			.append('text')
			.attr('transform', function (d) {
				const c = labelArc.centroid(d);
				return `translate(${c[0]},${c[1]})`;
			})
			.attr('dy', '.35em')
			.attr('text-anchor', 'middle')
			.text((d) => `${((d.data.duration / totalDuration) * 100).toFixed(1)}%`)
			.style('fill', 'var(--text-color)');

		// Add a legend to the bottom of the chart
		const legend = svg
			.append('g')
			.attr('transform', `translate(${-width / 2},${(radius * 2 + 100) / 2})`) // This positions the legend below the chart
			.attr('class', 'legend');

		const legendItem = legend
			.selectAll('.legend-item')
			.data(color.domain()) // Assuming color is your color scale and its domain is the publishers
			.enter()
			.append('g')
			.attr('class', 'legend-item')
			.attr('transform', (d, i) => `translate(0, ${i * 20})`); // This spaces out the legend items

		// Create colored rectangles for each legend item
		legendItem
			.append('rect')
			.attr('x', 10)
			.attr('width', 18)
			.attr('height', 18)
			.attr('fill', color);

		// Add text labels to each legend item
		legendItem
			.append('text')
			.attr('x', 35)
			.attr('y', 9)
			.attr('dy', '0.35em') // Vertically center the text
			.text((d) => d) // Set the label to the publisher's name
			.style('fill', 'var(--text-color)'); // Use CSS variable for text color

		// Update the height of the SVG to make room for the legend
		d3.select(chartContainer).select('svg').attr('height', 'auto');
		// .attr('height', height + legend.node().getBBox().height);

		// Dynamically adjust SVG height based on legend
		const legendHeight = legend.node().getBBox().height;
		d3.select(chartContainer)
			.select('svg')
			.attr('height', (radius + 20) * 2 + legendHeight + 200);
	}
</script>

<div
	bind:this={chartContainer}
	id="duration-pie-chart"
	class="chart-container"
	style="width: 100%; height: 100%;"
></div>

<style>
	.chart-container {
		box-sizing: border-box;
		overflow-y: scroll;
	}

	.chart-container::-webkit-scrollbar {
		width: 4px; /* Adjust the width to make the scrollbar thinner */
	}

	.chart-container::-webkit-scrollbar-track {
		background: #f1f1f1; /* The track (progress background) of the scrollbar */
	}

	.chart-container::-webkit-scrollbar-thumb {
		background: #888; /* The draggable scrolling handle */
	}

	.chart-container::-webkit-scrollbar-thumb:hover {
		background: #555; /* Color when hovering over the scrollbar */
	}
</style>
