<!-- src\lib\components\modals\NarrativesDatabaseWindow.svelte -->
<script lang="ts">
	import { slide } from 'svelte/transition';
	import {
		selectedNarrativesFiltersStore,
		narrativesPublisherOptionsStore
	} from '$lib/stores/narratives-stores';
	import { editPublisherOptions } from '$lib/api/narratives-api';
	import WorldMap from '$lib/json/WorldMap.json';

	import ChevronDownIcon from '$lib/components/icons/ChevronDownIcon.svelte';

	// Extracting unique country names from WorldMap
	$: countryOptions = Array.from(
		new Set(WorldMap.features.map((feature) => feature.properties.sovereignt))
	);

	$: selectedNarrativesFilters = $selectedNarrativesFiltersStore;
	// $: if (selectedNarrativesFilters) {
	// 	console.log('Updated selectedNarrativesFilters:', selectedNarrativesFilters);
	// }

	$: narrativesPublisherOptions = $narrativesPublisherOptionsStore;
	// $: if (narrativesPublisherOptions) {
	// 	console.log('narrativesPublisherOptions:', narrativesPublisherOptions);
	// }

	// Function to update the political orientation for a publisher
	function updatePoliticalOrientation(publisher, newOrientation) {
		narrativesPublisherOptions = narrativesPublisherOptions.map((option) => {
			if (option.publisher === publisher) {
				return { ...option, publisher_political_orientation: newOrientation };
			}
			return option;
		});
	}

	function updateCountry(country, newCountry) {
		narrativesPublisherOptions = narrativesPublisherOptions.map((option) => {
			if (option.country === country) {
				return { ...option, country: newCountry };
			}
			return option;
		});
	}

	// Function to update both political orientation and country
	async function applyChanges() {
		try {
			await editPublisherOptions(narrativesPublisherOptions);
			// console.log('Publisher options updated successfully');
			// Optionally, refresh data or give user feedback
		} catch (error) {
			console.error('Error updating publisher options:', error);
			// Handle error (show message to user, etc.)
		}
	}
</script>

<div class="filter-window" in:slide={{ duration: 300 }}>
	<table class="publishers-info-table">
		<thead>
			<tr>
				<th>Publisher</th>
				<th>Political Orientation</th>
				<th>Country</th>
			</tr>
		</thead>

		<tbody>
			{#each narrativesPublisherOptions as option}
				<tr>
					<td>{option.publisher}</td>

					<td class="select-container">
						<select
							bind:value={option.publisher_political_orientation}
							on:change={(event) =>
								updatePoliticalOrientation(option.publisher, event.target.value)}
						>
							{#each ['Far Left', 'Left', 'Lean Left', 'Centre', 'Lean Right', 'Right', 'Far Right', 'Independent', 'Unknown'] as orientation}
								<option value={orientation}>{orientation}</option>
							{/each}
						</select>
						<!-- <div class="icon-container">
                            <ChevronDownIcon />
                        </div> -->
					</td>

					<!-- This is the updated country dropdown cell -->
					<td class="select-container">
						<select
							bind:value={option.country}
							on:change={(event) => updateCountry(option.publisher, event.target.value)}
						>
							{#each countryOptions as country}
								<option value={country}>{country}</option>
							{/each}
						</select>
						<!-- <div class="icon-container">
                            <ChevronDownIcon />
                        </div> -->
					</td>
				</tr>
			{/each}
		</tbody>
	</table>

	<button on:click={applyChanges}>Apply Changes</button>
</div>

<style>
	.filter-window {
		position: absolute;
		/* top: 0; */
		left: 80px; /* Adjust this value to match the width of the left navbar */
		right: 80px; /* Adjust this value to match the width of the right navbar */
		max-height: 90vh; /* Limits the height of the modal to 90% of the viewport height */
		background-color: var(--navbar-bg-color);
		z-index: 10;
		box-shadow: var(--box-shadow);
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		transition: transform 0.3s ease-out;
		overflow-y: auto; /* Ensures a scrollbar is added when content overflows */
	}

	.publishers-info-table {
		width: 100%;
		margin-top: 20px;
		margin-bottom: 20px;
		border-collapse: collapse;
	}

	.select-container {
		position: relative;
		/* display: flex; */
		align-items: center;
	}

	.icon-container {
		height: 20px; /* Adjust as needed */
	}

	.publishers-info-table select {
		width: 100%; /* Make the select box take up the full cell width */
		height: 100%; /* Make the select box take up the full cell height */
		box-sizing: border-box;
		background-color: var(--navbar-bg-color); /* Set a background color */
		color: var(--color-text);
		-moz-appearance: none; /* Remove default styling in Firefox */
		-webkit-appearance: none; /* Remove default styling in Chrome and Safari */
		appearance: none; /* Remove default styling */
		cursor: pointer; /* Change cursor to indicate it's selectable */
		border: none;
		outline: none; /* Removes the default focus outline */
	}

	.publishers-info-table select:focus {
		border: none; /* Ensures no border appears on focus */
		box-shadow: none; /* Removes any focus-induced shadow, if present */
	}

	.publishers-info-table th,
	.publishers-info-table td {
		border: 1px solid var(--separator-line-color);
		padding: 8px 8px;
	}

	.publishers-info-table th {
		padding: 12px 8px;
		text-align: left;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		font-size: 20px;
	}

	button {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
	}

	.filter-window::-webkit-scrollbar {
		width: 4px; /* Adjust the width to make the scrollbar thinner */
		border-radius: 2px; /* Rounded edges */
	}

	.filter-window::-webkit-scrollbar-track {
		background: #f1f1f1; /* The track (progress background) of the scrollbar */
	}

	.filter-window::-webkit-scrollbar-thumb {
		background: #888; /* The draggable scrolling handle */
		border-radius: 2px; /* Rounded edges */
	}

	.filter-window::-webkit-scrollbar-thumb:hover {
		background: #555; /* Color when hovering over the scrollbar */
	}
</style>
