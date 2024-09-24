<!-- src\lib\components\charts\NarrativesPublisherPoliticalOrientation.svelte -->
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
	const margin = { top: 20, right: 30, bottom: 50, left: 65 };

	function updateDimensions() {
		width = chartContainer.clientWidth - margin.left - margin.right;
		height = chartContainer.clientHeight - margin.top - margin.bottom;
	}

	const orientationMap = {
		'Far Left': 'FL',
		'Left': 'L',
		'Lean Left': 'LL',
		'Centre': 'C',
		'Lean Right': 'LR',
		'Right': 'R',
		'Far Right': 'FR',
		'Independent': 'I',
		'Unknown': 'U'
	};

	const colorMap = {
		FL: '#08306b', // Dark Blue
		L: '#08519c', // Less Dark Blue
		LL: '#2171b5', // Lighter Blue
		C: '#bbbbbb', // Grey for Centre
		LR: '#cb181d', // Lighter Red
		R: '#a50f15', // Less Dark Red
		FR: '#67000d', // Dark Red
		I: '#F4D03F', // Light Grey for Independent
		U: '#aaaaaa' // Dark Grey for Unknown
	};

	function drawChart() {
		if (!chartContainer || !data) return;

		d3.select(chartContainer).selectAll('*').remove();

		const orientedData = data.map((d) => ({
			...d,
			publisher_political_orientation: orientationMap[d.publisher_political_orientation] || 'U'
		}));

		const orientationAggregate = d3.rollup(
			orientedData,
			(v) => d3.sum(v, (d) => d.duration),
			(d) => d.publisher_political_orientation
		);

		const totalDuration = d3.sum(Array.from(orientationAggregate.values()));

		const dataArray = Array.from(orientationAggregate, ([key, value]) => ({
			orientation: key,
			percentage: (value / totalDuration) * 100
		}));

		dataArray.sort(
			(a, b) =>
				Object.keys(orientationMap).indexOf(a.orientation) -
				Object.keys(orientationMap).indexOf(b.orientation)
		);

		updateDimensions();

		const svg = d3
			.select(chartContainer)
			.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		const y = d3
			.scaleLinear()
			.domain([0, d3.max(dataArray, (d) => d.percentage) || 100])
			.range([height, 0]);

		svg.append('g').call(d3.axisLeft(y));

		// Define a fixed array for the X-axis categories in the desired order
		const xCategories = ['FL', 'L', 'LL', 'C', 'LR', 'R', 'FR', 'I', 'U'];

		const x = d3
			.scaleBand()
			.range([0, width])
			.domain(xCategories) // Use the fixed array for the domain
			.padding(0.1);

		svg.append('g').attr('transform', `translate(0,${height})`).call(d3.axisBottom(x));

		svg
			.selectAll('.bar')
			.data(dataArray, (d) => d.orientation) // Key function to match data by orientation
			.enter()
			.append('rect')
			.attr('class', 'bar')
			.attr('x', (d) => x(d.orientation))
			.attr('y', (d) => y(d.percentage))
			.attr('width', x.bandwidth())
			.attr('height', (d) => height - y(d.percentage))
			.attr('fill', (d) => colorMap[d.orientation]);

		// Y-axis label
		svg
			.append('text')
			.attr('transform', 'rotate(-90)')
			.attr('y', -margin.left + 22) // Adjust the position based on your margin
			.attr('x', 0 - height / 2)
			.attr('dy', '1em')
			.style('text-anchor', 'middle')
			.text('(%)')
			.style('fill', 'var(--text-color)'); // Use CSS variable for text color
	}
</script>

<div
	bind:this={chartContainer}
	id="publisher-political-orientation-bar-chart"
	style="width: 100%; height: 100%;"
></div>
