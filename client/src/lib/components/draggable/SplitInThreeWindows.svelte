<!-- src\lib\components\draggable\SplitInThreeWindows.svelte -->

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Split from 'split.js';

	import NarrativesStackedBars from '$lib/components/charts/NarrativesStackedBars.svelte';
	import NarrativesSummary from '$lib/components/cards/NarrativesSummary.svelte';
	import NarrativesDurationPie from '$lib/components/charts/NarrativesDurationPie.svelte';

	let splitInstance;

	export let dataStore; // Accept the store

	let pane1, pane2, pane3; // Pane references

	onMount(() => {
		// Ensure Split.js is correctly initialized with dynamic pane references
		splitInstance = Split([pane1, pane2, pane3], {
			sizes: [15, 60, 25], // Initial percentage sizes for each pane
			minSize: 100,        // Minimum size in pixels for each pane
			gutterSize: 10,      // Size of the gutter in pixels
			cursor: 'col-resize', // Cursor to display while dragging
			direction: 'horizontal', // Direction of the split
			onDrag: (sizes) => {
				// Optionally handle sizes during drag
			},
			onDragEnd: () => {
				// Optionally handle after dragging is done
			}
		});
	});

	// Cleanup on component destroy
	onDestroy(() => {
		if (splitInstance) {
			splitInstance.destroy();
		}
	});
</script>

<div class="split-container">
	<!-- Dynamically bind the pane divs to variables -->
	<div bind:this={pane1} class="split-pane">
		<NarrativesDurationPie dataStore={dataStore} />
	</div>
	<div bind:this={pane2} class="split-pane">
		<NarrativesStackedBars dataStore={dataStore} />
	</div>
	<div bind:this={pane3} class="split-pane">
		<NarrativesSummary dataStore={dataStore} />
	</div>
</div>

<style>
	.split-container {
		display: flex;
		flex-direction: row;
		height: 100%;  /* Ensure the container takes up the full height */
		width: 100%;   /* Ensure the container takes up the full width */
		position: relative;  /* Make sure gutters stay within the container */
	}

	.split-pane {
		overflow: auto;      /* Enable scrolling if content overflows */
		width: 0;            /* Split.js will handle the width of each pane */
		min-width: 100px;     /* Minimum width for each pane */
	}

	/* Global styles for gutters */
	:global(.gutter) {
		transition: background-color 0.2s ease; /* Smooth background color transition for hover effect */
	}

	:global(.gutter.gutter-horizontal) {
		display: flex; /* Enable flexbox */
		align-items: center; /* Center vertically */
		justify-content: center; /* Center horizontally */
		cursor: ew-resize; /* The east-west resize cursor */
		border-left: 1px solid #aaa;
		border-right: 1px solid #aaa;
		padding: 0 5px;
	}

	/* Hover effect for the gutters */
	:global(.gutter:hover) {
		background-color: #bbb; /* Darker color on hover for feedback */
	}

	/* Visual cue for the draggable gutters */
	:global(.gutter.gutter-horizontal::after) {
		content: '⋮⋮'; /* Vertical ellipsis as a grip icon */
		color: #888; 
		font-size: 16px; /* Larger font size to make it clear */
		line-height: 1; /* Tight line height to prevent extra vertical space */
		pointer-events: none; /* Ensures the icon doesn't interfere with dragging */
		border-radius: 10px; /* Rounded edges for the icon's container */
		padding: 4px; /* Padding around the icon */
		height: 30px; /* Total height of the icon's container, adjust as needed */
		width: 30px; /* Total width of the icon's container, adjust as needed */
		display: flex; /* Use flexbox to center the content */
		align-items: center; /* Center the content vertically */
		justify-content: center; /* Center the content horizontally */
		margin: 0; /* Remove any margin */
	}
</style>
