<!-- src\lib\components\charts\NarrativesStackedBars.svelte -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
    import * as d3 from 'd3';
    import { browser } from '$app/environment';
    import { groupNarrativesByDatePublishedAndPublisher } from '$lib/utils/narratives-utils';
	import { derived } from 'svelte/store';

    export let dataStore; // Accept the store as a prop

    // Create a local derived store from dataStore using the utility function
    const groupedNarrativesStore = derived(dataStore, ($dataStore) => {
        return groupNarrativesByDatePublishedAndPublisher($dataStore);
    });

    let chartContainer: HTMLElement;
    let data = [];

    // Subscribe to the derived store and update data reactively
    groupedNarrativesStore.subscribe((value) => {
        data = value;
        drawChart();
    });

	onMount(() => {
		if (browser) {
			// Check if running in the browser
			drawChart();
			window.addEventListener('resize', drawChart);
		}
	});

	onDestroy(() => {
		if (browser) {
			// Check if running in the browser
			window.removeEventListener('resize', drawChart);
		}
	});

	function drawChart() {
		if (!chartContainer || !data) return;

		const dateProcessed = Object.entries(data);

		// Calculate the number of unique dates
		const uniqueDates = new Set(dateProcessed.map((d) => d));
		const numberOfUniqueDates = uniqueDates.size;

		d3.select(chartContainer).selectAll('*').remove();

		const margin = { top: 0, right: 0, bottom: 40, left: 20 };
		// const width = chartContainer.clientWidth - margin.left - margin.right;
		const width = 100 * numberOfUniqueDates;
		const height = chartContainer.clientHeight - margin.top - margin.bottom;

		const svg = d3
			.select(chartContainer)
			.append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		const parseDate = d3.utcParse('%Y-%m-%d');

		const dataProcessed = Object.entries(data)
			.map(([date, entries]) => {
				return entries.map((entry) => ({
					date: parseDate(entry.date_published),
					publisher: entry.publisher,
					duration: entry.duration.map(Number),
					content_ids: entry.content_ids,
					itemOrder: entry.itemOrder,
					titles: entry.titles
				}));
			})
			.flat();

		dataProcessed.sort((a, b) => a.date - b.date);

		const durationByPublisher = d3.rollup(dataProcessed, 
			(entries) => d3.sum(entries, entry => d3.sum(entry.duration)), // Sum all durations
			entry => entry.publisher);

		const sortedPublishers = Array.from(durationByPublisher, ([publisher, duration]) => ({ publisher, duration }))
			.sort((a, b) => b.duration - a.duration)
			.map(d => d.publisher);

		const dateValues = [...new Set(dataProcessed.map((d) => d.date))];
		const xScale = d3.scaleBand().domain(dateValues).range([0, width]).padding(0.1);

		// Calculate the max itemOrder value for setting up the y-axis
		const maxItemOrder = d3.max(dataProcessed, (d) => d3.max(d.itemOrder));
		const fixedBarWidth = 80;
		const fixedBarHeight = 80;

		// Since the height of each bar is 50, we'll create a scale that maps itemOrder to pixel position
		const yScale = d3
			.scaleLinear()
			.domain([0, maxItemOrder])
			.range([height, height - fixedBarHeight * maxItemOrder]); // Subtract 50 to align the first bar's top with the first tick

		const colorScale = d3.scaleOrdinal()
			.domain(sortedPublishers)
			.range(d3.schemeCategory10);

		// const colorScale = d3
		// 	.scaleOrdinal()
		// 	.domain(dataProcessed.map((d) => d.publisher))
		// 	.range(d3.schemeCategory10);

		function handleBarClick(content_id) {
			const event = new CustomEvent('barclick', {
				detail: { content_id },
				bubbles: true // This allows the event to bubble up through the DOM
			});

			// Dispatch the event from the SVG element itself or from `svg.node()`
			svg.node().dispatchEvent(event);
		}

		dataProcessed.forEach((entry, entryIndex) => {
			entry.content_ids.forEach((content_id, index) => {
				const order = entry.itemOrder[index];
				const barX = xScale(entry.date) + xScale.bandwidth() / 2 - fixedBarWidth / 2;
				const barY = height - order * fixedBarHeight;

				// Unique ID for each clipPath to match bars with their text
				const clipPathId = `clip-${entryIndex}-${index}`;

				// Define a clipPath for each bar
				svg
					.append('clipPath')
					.attr('id', clipPathId)
					.append('rect')
					.attr('x', barX)
					.attr('y', barY)
					.attr('width', fixedBarWidth)
					.attr('height', fixedBarHeight);

				// Draw the bar
				const bar = svg
					.append('rect')
					.attr('x', barX)
					.attr('y', barY)
					.attr('width', fixedBarWidth)
					.attr('height', fixedBarHeight)
					.attr('rx', 5)
					.attr('ry', 5)
					.attr('fill', colorScale(entry.publisher))
					.attr('stroke', 'black')
					.attr('stroke-width', 1);

				// Add hover effect
				bar
					.on('mouseover', function () {
						d3.select(this).transition().duration(10).attr('opacity', 0.7);
					})
					.on('mouseout', function () {
						d3.select(this).transition().duration(10).attr('opacity', 1);
					});

				bar.append('title').text(content_id);
				bar.on('click', () => handleBarClick(content_id));

				// Adding publisher text inside each bar
				const text = svg
					.append('text')
					.attr('clip-path', `url(#${clipPathId})`)
					.attr('x', barX + fixedBarWidth / 2) // Initially, center the text horizontally
					.attr('y', barY + fixedBarHeight / 2) // Center the text vertically
					.attr('text-anchor', 'middle') // Ensure the text is centered
					.attr('dominant-baseline', 'central')
					.text(entry.publisher)
					.attr('fill', 'white')
					.attr('font-size', '12px');

				const textWidth = text.node().getComputedTextLength();

				// Apply the sliding animation only if the text width exceeds the bar width
				if (textWidth > fixedBarWidth) {
					text.attr('x', barX).attr('text-anchor', 'start'); // Adjust start position for sliding effect

					// Slide the text
					function slideText() {
						text
							.transition()
							.duration(3000)
							.attr('x', barX - textWidth + fixedBarWidth) // Slide to the left
							.ease(d3.easeLinear)
							.on('end', function () {
								d3.select(this)
									.transition()
									.duration(1000) // Pause at the end
									.on('end', function () {
										d3.select(this)
											.attr('x', barX) // Reset to the start position
											.each(slideText); // Repeat the animation
									});
							});
					}
					slideText();
				}
			});
		});

		// Use UTC time format for the x-axis
		const utcFormat = d3.utcFormat('%d/%m/%Y');
		const xAxis = d3.axisBottom(xScale).tickFormat((d) => utcFormat(d));

		svg.append('g').attr('transform', `translate(0,${height})`).call(xAxis);

		// Setup the y-axis with ticks from 1 to maxItemOrder
		const yAxis = d3.axisLeft(yScale).ticks(maxItemOrder);
		svg.append('g').call(yAxis);
	}
</script>

<div>
	<h3 class="chart-title">Timeline</h3>
</div>

<div
	bind:this={chartContainer}
	id="stacked-bar-chart"
	class="chart-container"
	style="width: 100%; height: 88%;"
>
	<!-- The chart will be drawn inside this div -->
</div>

<style>
	.chart-container {
		/* padding: 15px; */
		box-sizing: border-box; /* Ensures padding doesn't add to the width */
		overflow-x: scroll;
		overflow-y: hidden;
	}

	.chart-title {
		text-align: center;
		margin-top: 15px;
		/* margin-bottom: 10px; */
	}

	.chart-container::-webkit-scrollbar {
		height: 4px; /* Adjust the width to make the scrollbar thinner */
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
