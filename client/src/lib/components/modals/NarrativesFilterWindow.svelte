<!-- src\lib\components\modals\NarrativesFilterWindow.svelte -->
<script lang="ts">
	import { slide } from 'svelte/transition';
	import {
		narrativesStore,
		selectedNarrativesFiltersStore,
		narrativesPublisherOptionsStore
	} from '$lib/stores/narratives-stores';

	$: narratives = $narrativesStore; // Reactive subscription to narrativesStore
	$: selectedNarrativesFilters = $selectedNarrativesFiltersStore;
	$: narrativesPublisherOptions = $narrativesPublisherOptionsStore;

	export let handleFilterChange;

	$: publishers = narrativesPublisherOptions.map((option) => option.publisher);
	let platforms = ['Web', 'Nostr', 'Twitter', 'YouTube'];
	// $: platforms = Array.from(new Set(narratives.map(option => option.platform)))
	// let countries = ['United Kingdom', 'United States of America', 'France', 'Italy'];
	// $: countries = narrativesPublisherOptions.map(option => option.country);
	$: countries = Array.from(new Set(narrativesPublisherOptions.map((option) => option.country)));
	$: macro_topics = Array.from(new Set(narratives.map((option) => option.macro_topic)));
	// let macro_topics = ['House prices'];

	let showPublisherDropdown = false;
	let showPlatformDropdown = false;
	let showCountryDropdown = false;
	let showMacroTopicDropdown = false;

	// Search inputs
	let searchPublisher = '';
	let searchPlatform = '';
	let searchCountry = '';
	let searchMacroTopic = '';

	// Select all / deselect all functionality
	function selectAll(list, selectedList) {
		// Clear the array and push all elements to trigger reactivity
		selectedList.length = 0;
		selectedList.push(...list);
		selectedNarrativesFiltersStore.update((filters) => ({ ...filters })); // Force reactivity
	}

	function deselectAll(selectedList) {
		// Empty the array
		selectedList.length = 0;
		selectedNarrativesFiltersStore.update((filters) => ({ ...filters })); // Force reactivity
	}

	function applyFilters() {
		selectedNarrativesFiltersStore.set(selectedNarrativesFilters);
		handleFilterChange(selectedNarrativesFilters);
	}

	function toggleDropdown(dropdownName) {
		if (dropdownName === 'publisher') showPublisherDropdown = !showPublisherDropdown;
		if (dropdownName === 'platform') showPlatformDropdown = !showPlatformDropdown;
		if (dropdownName === 'country') showCountryDropdown = !showCountryDropdown;
		if (dropdownName === 'macro topic') showMacroTopicDropdown = !showMacroTopicDropdown;
	}
</script>

<div class="filter-window" in:slide={{ duration: 300 }}>
	<div class="filters-row">
		<div class="filter-section">
			<label class="filter-label">Publishers</label>
			<button on:click={() => toggleDropdown('publisher')}>Select Publisher</button>
			{#if showPublisherDropdown}
				<div class="filter-dropdown">
					<input type="text" bind:value={searchPublisher} placeholder="Search publishers..." />
					<button on:click={() => selectAll(publishers, selectedNarrativesFilters.publishers)}
						>Select All</button
					>
					<button on:click={() => deselectAll(selectedNarrativesFilters.publishers)}
						>Deselect All</button
					>
					{#each publishers.filter((pub) => pub && pub
								.toLowerCase()
								.includes(searchPublisher.toLowerCase())) as publisher}
						<label>
							<input
								type="checkbox"
								bind:group={selectedNarrativesFilters.publishers}
								value={publisher}
							/>
							{publisher}
						</label>
					{/each}
				</div>
			{/if}
		</div>

		<div class="filter-section">
			<label class="filter-label">Platforms</label>
			<button on:click={() => toggleDropdown('platform')}>Select Platforms</button>
			{#if showPlatformDropdown}
				<div class="filter-dropdown">
					<input type="text" bind:value={searchPlatform} placeholder="Search platforms..." />
					<button on:click={() => selectAll(platforms, selectedNarrativesFilters.platforms)}
						>Select All</button
					>
					<button on:click={() => deselectAll(selectedNarrativesFilters.platforms)}
						>Deselect All</button
					>
					{#each platforms.filter((platform) => platform && platform
								.toLowerCase()
								.includes(searchPlatform.toLowerCase())) as platform}
						<label>
							<input
								type="checkbox"
								bind:group={selectedNarrativesFilters.platforms}
								value={platform}
							/>
							{platform}
						</label>
					{/each}
				</div>
			{/if}
		</div>

		<div class="filter-section">
			<label class="filter-label">Countries</label>
			<button on:click={() => toggleDropdown('country')}>Select Countries</button>
			{#if showCountryDropdown}
				<div class="filter-dropdown">
					<input type="text" bind:value={searchCountry} placeholder="Search countries..." />
					<button on:click={() => selectAll(countries, selectedNarrativesFilters.countries)}
						>Select All</button
					>
					<button on:click={() => deselectAll(selectedNarrativesFilters.countries)}
						>Deselect All</button
					>
					{#each countries.filter((country) => country && country
								.toLowerCase()
								.includes(searchCountry.toLowerCase())) as country}
						<label>
							<input
								type="checkbox"
								bind:group={selectedNarrativesFilters.countries}
								value={country}
							/>
							{country}
						</label>
					{/each}
				</div>
			{/if}
		</div>

		<div class="filter-section">
			<label class="filter-label">Macro Topic</label>
			<button on:click={() => toggleDropdown('macro topic')}>Select Macro Topic</button>
			{#if showMacroTopicDropdown}
				<div class="filter-dropdown">
					<input type="text" bind:value={searchMacroTopic} placeholder="Search macro topics..." />
					<button on:click={() => selectAll(macro_topics, selectedNarrativesFilters.macro_topics)}
						>Select All</button
					>
					<button on:click={() => deselectAll(selectedNarrativesFilters.macro_topics)}
						>Deselect All</button
					>
					{#each macro_topics.filter((topic) => topic && topic
								.toLowerCase()
								.includes(searchMacroTopic.toLowerCase())) as macro_topic}
						<label>
							<input
								type="checkbox"
								bind:group={selectedNarrativesFilters.macro_topics}
								value={macro_topic}
							/>
							{macro_topic}
						</label>
					{/each}
				</div>
			{/if}
		</div>

		<!-- Date Added Range -->
		<div class="filter-section">
			<label class="filter-label">Date Added</label>
			<div class="date-inputs">
				<label
					>From:
					<input type="date" bind:value={selectedNarrativesFilters.dateAddedRange.start} />
				</label>
				<label
					>To:
					<input type="date" bind:value={selectedNarrativesFilters.dateAddedRange.end} />
				</label>
			</div>
		</div>

		<!-- Date Published Range -->
		<div class="filter-section">
			<label class="filter-label">Date Published</label>
			<div class="date-inputs">
				<label
					>From:
					<input type="date" bind:value={selectedNarrativesFilters.datePublishedRange.start} />
				</label>
				<label
					>To:
					<input type="date" bind:value={selectedNarrativesFilters.datePublishedRange.end} />
				</label>
			</div>
		</div>
	</div>
	<button on:click={applyFilters}>Apply Filter</button>
</div>

<style>
	.filter-window {
		position: absolute;
		/* top: 0; */
		left: 80px;
		right: 80px;
		height: auto;
		background-color: var(--navbar-bg-color);
		z-index: 10;
		box-shadow: var(--box-shadow);
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		transition: transform 0.3s ease-out;
	}

	.filters-row {
		display: flex;
		justify-content: space-around;
		align-items: center;
		flex-wrap: wrap;
		margin-bottom: 20px;
		justify-content: start; /* Align to the start of the main axis */
		align-items: start; /* Align to the start of the cross axis */
		gap: 50px;
	}

	.filter-section {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		margin-bottom: 15px;
	}

	.filter-label {
		font-size: 20px;
		margin-bottom: 5px;
		font-weight: bold;
		text-align: center;
		align-self: center;
	}

	.filter-dropdown {
		position: absolute; /* Takes the dropdown out of the normal document flow */
		z-index: 100; /* Ensures the dropdown is on top of other content */
		width: auto; /* Allows the dropdown to expand based on content width */
		min-width: 150px; /* Minimum width of the dropdown */
		max-width: 300px; /* Adjust this to the width that fits your longest text */
		max-height: 400px; /* Adjust this value based on your design needs */
		overflow-y: auto; /* Enables vertical scrolling */
		overflow-x: hidden; /* Prevents horizontal scrolling */
		white-space: nowrap; /* Prevents text from wrapping onto multiple lines */
		text-overflow: ellipsis; /* Adds an ellipsis if the text is too long */
		top: 100%; /* Positions the dropdown right below the toggle button */
		left: 0; /* Aligns the dropdown with the left edge of the filter section */
		display: flex;
		flex-direction: column;
		padding: 10px;
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		/* border-radius: 8px; */
	}

	.date-inputs {
		display: flex;
		flex-direction: column; /* Stack items vertically */
		align-items: flex-end; /* Align items to the right */
		gap: 10px; /* Adds space between "From" and "To" date inputs */
	}

	label {
		margin: 5px 0;
	}

	input[type='checkbox'] {
		margin-right: 10px;
	}

	input[type='date'] {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
		display: flex;
		align-items: flex-end; /* Align items to the right */
	}

	button {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
	}

	.filter-dropdown::-webkit-scrollbar {
		width: 4px; /* Adjust the width to make the scrollbar thinner */
		border-radius: 2px; /* Rounded edges */
	}

	.filter-dropdown::-webkit-scrollbar-track {
		background: #f1f1f1; /* The track (progress background) of the scrollbar */
	}

	.filter-dropdown::-webkit-scrollbar-thumb {
		background: #888; /* The draggable scrolling handle */
		border-radius: 2px; /* Rounded edges */
	}

	.filter-dropdown::-webkit-scrollbar-thumb:hover {
		background: #555; /* Color when hovering over the scrollbar */
	}
</style>
