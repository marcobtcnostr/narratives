<!-- src\lib\components\cards\Summary.svelte -->

<script lang="ts">
	import { narrativesStore, selectedContentIDStore } from '$lib/stores/narratives-stores';
	import { onMount } from 'svelte';
	import LightningChargeIcon from '$lib/components/icons/LightningChargeIcon.svelte';
	import AlarmIcon from '$lib/components/icons/AlarmIcon.svelte';
	import { writable, get } from 'svelte/store';

	import { updateContentIdTopic } from '$lib/api/narratives-api';

	// let data;
	// narrativesStore.subscribe((value) => {
	// 	data = value;
	// });

	export let dataStore; // Accept the store
	let data = [];

	onMount(() => {

		dataStore.subscribe((value) => {
				data = value;
			});

		const chartContainer = document.getElementById('stacked-bar-chart');
		if (chartContainer) {
			chartContainer.addEventListener('barclick', handleBarClickEvent);
		}
	});

	function handleBarClickEvent(event) {
		selectedContentIDStore.set(event.detail.content_id);
	}

	let title = 'Select an item';
	let transcript = '';
	let summary = '';
	let date_published = '';
	let macro_topic = 'Unknown';
	let reference_image = '';

	let inputTopic = writable(''); //

	let viewMode = 'summary';

	// Function to parse the summary
	function parseSummary(summary) {
		// Check if summary is empty or null
		if (!summary || summary.trim() === '') {
			return []; // Return an empty array or any other default value as needed
		}

		const sections = summary.split('\n\n');
		return sections.map((section) => {
			const [title, ...contentLines] = section.split('\n');
			return {
				title: title.replace(':', '').trim(),
				content: contentLines.join('<br>') // Using <br> to create line breaks
			};
		});
	}

	let parsedSummary = [];

	selectedContentIDStore.subscribe((selectedContentID) => {
		if (selectedContentID && data) {
			const matchingData = data.find((d) => d.content_id === selectedContentID);
			if (matchingData) {
				title = matchingData.title || 'No title found for selected content';
				transcript = matchingData.transcript || 'No transcript found for selected content';
				summary = matchingData.summary || 'No summary found for selected content';
				date_published =
					matchingData.date_published || 'No date published found for selected content';
				macro_topic = matchingData.macro_topic || 'Unknown';
				reference_image =
					matchingData.reference_image || 'No reference image found for selected content';
				parsedSummary = parseSummary(matchingData.summary);
			}
		}
	});

	// Action handlers for the icons
	function onChargeClick() {
		console.log('Lightning Charge clicked');
		// Implement your action here
	}

	function onAlarmClick() {
		console.log('Alarm clicked');
		// Implement your action here
	}

	function toggleView(mode) {
		viewMode = mode;
	}

	function applyTopic() {
		const newTopic = $inputTopic;
		const contentId = $selectedContentIDStore;
		macro_topic = newTopic; // Apply the entered topic to the displayed topic

		updateContentIdTopic(contentId, newTopic) // Call the API to update the topic in the backend
			.then(() => {
				console.log('Topic updated successfully');
			})
			.catch((error) => {
				console.error('Failed to update topic:', error);
			});

		inputTopic.set(''); // Optionally reset the input after applying
	}
</script>

<div class="summary-container">
	<!-- <h3 class="chart-title">AI Summary</h3> -->

	<div class="content-row">
		{#if reference_image}
			<img src={reference_image} alt="Reference Image" />
		{/if}
		{#if reference_image}
			<ul class="button-list">
				<li><button on:click={onChargeClick}><LightningChargeIcon /></button></li>
				<li><button on:click={onAlarmClick}><AlarmIcon /></button></li>
			</ul>
		{/if}
	</div>

	<h4>{title}</h4>

	{#if transcript}
		<h5>{date_published}</h5>

		<div class="topic-input">
			<h5>Topic:</h5>
			<input bind:value={$inputTopic} placeholder={macro_topic} />
			<button on:click={applyTopic}>Apply</button>
		</div>

		<div class="view-buttons">
			<button on:click={() => toggleView('summary')} class:active={viewMode === 'summary'}
				>Summary</button
			>
			<button on:click={() => toggleView('original')} class:active={viewMode === 'original'}
				>Original</button
			>
		</div>
	{/if}

	{#if viewMode === 'summary'}
		{#each parsedSummary as section}
			<h6>{section.title}</h6>
			<p>{@html section.content}</p>
		{/each}
	{:else}
		<p>{@html transcript}</p>
	{/if}
</div>

<style>
	.summary-container {
		background-color: var(--event-card-bg);
		padding: 15px;
		box-shadow: var(--box-shadow);
		overflow-y: scroll;
		height: 500px;
	}

	.chart-title {
		text-align: center;
		margin-top: 0px;
		margin-bottom: 10px;
	}

	.content-row {
		display: flex;
		align-items: start;
	}

	.button-list {
		list-style: none;
		padding: 0;
		margin-left: 20px;
		display: flex;
		flex-direction: column;
		width: 60px;
	}

	.button-list li {
		margin-bottom: 10px;
	}

	.button-list button {
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		border: none;
		padding: 8px;
		border-radius: 8px;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.button-list button:hover {
		background-color: var(--button-hover-bg-color);
		color: var(--button-hover-text-color);
	}

	.view-buttons {
		display: flex;
		margin-top: 10px;
		margin-bottom: 10px;
		gap: 10px;
	}

	.view-buttons button {
		flex: 1;
		padding: 10px;
		font-size: 16px;
		border: 1px solid #ccc;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		cursor: pointer;
		border-radius: 5px;
		box-shadow: var(--box-shadow);
	}

	.view-buttons button:hover {
		background-color: var(--button-hover-bg-color);
		color: var(--button-hover-text-color);
	}

	.view-buttons button.active {
		background-color: var(--button-active-bg-color);
		color: var(--button-active-text-color);
	}

	.topic-input {
		display: flex;
		margin-top: 10px;
		margin-bottom: 10px;
		align-items: center; /* Ensures vertical alignment of the input and button */
	}

	.topic-input input {
		/* flex: 1;  */
		padding: 8px;
		border: 1px solid #ccc;
		border-radius: 4px;
		margin-right: 10px; /* Space between input and button */
		margin-left: 10px; /* Space between input and button */
		max-width: 50%;
		color: black;
	}

	.topic-input button {
		padding: 8px;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		border: none;
		border-radius: 4px;
		cursor: pointer;
		box-shadow: var(--box-shadow);
	}

	.topic-input button:hover {
		background-color: var(--button-hover-bg-color);
		color: var(--button-hover-text-color);
	}

	/* .summary-container::-webkit-scrollbar {
		display: none;
	} */

	.summary-container::-webkit-scrollbar {
		width: 4px; /* Adjust the width to make the scrollbar thinner */
	}

	.summary-container::-webkit-scrollbar-track {
		background: #f1f1f1; /* The track (progress background) of the scrollbar */
	}

	.summary-container::-webkit-scrollbar-thumb {
		background: #888; /* The draggable scrolling handle */
	}

	.summary-container::-webkit-scrollbar-thumb:hover {
		background: #555; /* Color when hovering over the scrollbar */
	}

	.summary-container img {
		border-radius: 8px; /* This applies rounded corners to the image */
		width: 80%;
		max-width: 500px; /* This ensures the image is responsive and fits the container */
		height: auto; /* This maintains the aspect ratio of the image */
		margin-bottom: 20px;
	}
</style>
