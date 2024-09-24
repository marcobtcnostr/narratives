<!-- src\lib\components\draggable\SplitInThreeWindows.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import Split from 'split.js';

	import NarrativesOpenAIChatbot from '$lib/components/cards/NarrativesOpenAIChatbot.svelte';
	import NarrativesOpenAIInstructions from '$lib/components/cards/NarrativesOpenAIInstructions.svelte';

	let splitInstance;

	onMount(() => {
		splitInstance = Split(['#pane4', '#pane5'], {
			sizes: [30, 70], // Initial percentage sizes for each pane
			minSize: 100, // Minimum size in pixels for each pane
			gutterSize: 10, // Size of the gutter in pixels
			cursor: 'col-resize', // Cursor to display while dragging
			direction: 'horizontal', // Direction of the split
			onDrag: function (sizes) {
				// This function is called repeatedly as the gutters are dragged
				// console.log(sizes); 
			},
			onDragEnd: function () {
				// This function is called once when the gutter is released
				// console.log('Finished dragging');
			}
		});
		// console.log(splitInstance);
	});

	// Optional: Cleanup if your component is destroyed
	import { onDestroy } from 'svelte';
	onDestroy(() => {
		if (splitInstance) {
			splitInstance.destroy();
		}
	});
</script>

<div class="split-container">
	<div id="pane4" class="split-pane">
		<NarrativesOpenAIInstructions />
	</div>
	<div id="pane5" class="split-pane">
		<NarrativesOpenAIChatbot />
	</div>
</div>

<style>
	.split-container {
		display: flex;
		flex-direction: row;
		height: auto;
	}

	.split-pane {
		min-width: 100px; /* Minimum width for each pane */
		overflow: auto;
	}

	/* Global styles for gutters */
	:global(.gutter) {
		/* background-color: #ccc;  */
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
		/* background-color: #f0f0f0;  */
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
