<!-- src\lib\components\pages\NarrativesDashboard.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import GenericCarousel from '$lib/components/carousel/GenericCarousel.svelte';
	import NarrativesStackedBars from '$lib/components/charts/NarrativesStackedBars.svelte';
	import NarrativesDurationBars from '$lib/components/charts/NarrativesDurationBars.svelte';
	import NarrativesCountryBars from '$lib/components/charts/NarrativesCountryBars.svelte';
	import NarrativesTopicBars from '$lib/components/charts/NarrativesTopicBars.svelte';
	import NarrativesPublisherPoliticalOrientation from '$lib/components/charts/NarrativesPublisherPoliticalOrientation.svelte';
	import NarrativesWorldMap from '$lib/components/charts/NarrativesWorldMap.svelte';
	import SplitInThreeWindows from '$lib/components/draggable/SplitInThreeWindows.svelte';
	import SplitInTwoWindows from '$lib/components/draggable/SplitInTwoWindows.svelte';

	import {
		narrativesStore,
		isNarrativesFilterWindowOpen,
		isNarrativesDatabaseWindowOpen,
		isNarrativesDatabaseAddWindowOpen,
		isShareNarrativesPostWindowOpen,
		isUpdatingDatabase,
		groupedNarrativesByDatePublishedAndPublisherStore,
		selectedNarrativesFiltersStore,
		narrativesPublisherOptionsStore
	} from '$lib/stores/narratives-stores';

	import { fetchNarrativesData, fetchNarrativesPublisherOptions } from '$lib/api/narratives-api';

	import NarrativesFilterWindow from '$lib/components/modals/NarrativesFilterWindow.svelte';
	import NarrativesDatabaseWindow from '$lib/components/modals/NarrativesDatabaseWindow.svelte';
	import NarrativesDatabaseAddWindow from '$lib/components/modals/NarrativesDatabaseAddWindow.svelte';
	import ShareNarrativesPostWindow from '$lib/components/modals/ShareNarrativesPostWindow.svelte';

	import { groupNarrativesByDatePublishedAndPublisher } from '$lib/utils/narratives-utils';

	import Spinner from '$lib/components/icons/Spinner.svelte';
	export let dataStore = narrativesStore;

	let images = [];

	let components = [
		{ id: 1, type: 'component', component: NarrativesCountryBars },
		{ id: 2, type: 'component', component: NarrativesWorldMap },
		{ id: 3, type: 'component', component: NarrativesPublisherPoliticalOrientation },
		{ id: 4, type: 'component', component: NarrativesDurationBars },
		{ id: 5, type: 'component', component: NarrativesTopicBars }
	];

	$: narratives = $narrativesStore; // Reactive subscription to narrativesStore
	// $: if (narratives) {
	// 	console.log('Updated narratives:', narratives);
	// }

	$: narrativesByDatePublishedAndPublisher = $groupedNarrativesByDatePublishedAndPublisherStore;
	// $: if (narrativesByDatePublishedAndPublisher) {
	// 	console.log('Updated narrativesByDatePublishedAndPublisher:', narrativesByDatePublishedAndPublisher);
	// }

	$: selectedNarrativesFilters = $selectedNarrativesFiltersStore;
	// $: if (selectedNarrativesFilters) {
	// 	console.log('Updated selectedNarrativesFilters:', selectedNarrativesFilters);
	// }

	$: narrativesPublisherOptions = $narrativesPublisherOptionsStore;
	// $: if (narrativesPublisherOptions) {
	// 	console.log('narrativesPublisherOptions:', narrativesPublisherOptions);
	// }

	$: IsUpdatingDatabase = $isUpdatingDatabase;
	// $: if (IsUpdatingDatabase) {
	// 	console.log('IsUpdatingDatabase:', IsUpdatingDatabase);
	// }

	onMount(async () => {
		await fetchNarrativesData(selectedNarrativesFilters);
		await fetchNarrativesPublisherOptions();
	});

	async function handleFilterChange(selectedNarrativesFilters) {
		await fetchNarrativesData(selectedNarrativesFilters);
	}
</script>

{#if $isNarrativesFilterWindowOpen}
	<NarrativesFilterWindow {handleFilterChange} />
{/if}

{#if $isNarrativesDatabaseWindowOpen}
	<NarrativesDatabaseWindow />
{/if}

{#if $isNarrativesDatabaseAddWindowOpen}
	<NarrativesDatabaseAddWindow />
{/if}

{#if $isShareNarrativesPostWindowOpen}
	<ShareNarrativesPostWindow />
{/if}

{#if $isUpdatingDatabase}
	<div class="updating-database-popup">
		<div class="spinner-border text-success" role="status">
			<!-- <span class="sr-only"></span> -->
			<Spinner />
		</div>

		<div>Updating database ...</div>
	</div>
{/if}

<!-- <h1>Dashboard</h1> -->

<div class="flex flex-col h-screen overflow">
	<div style="box-shadow: var(--box-shadow);">
		<GenericCarousel {images} {components} dataStore={dataStore}/>
	</div>

	<div style="box-shadow: var(--box-shadow);">
		<SplitInThreeWindows {images} {components} dataStore={dataStore}/>
	</div>

	<div style="box-shadow: var(--box-shadow);">
		<SplitInTwoWindows {images} {components}/>
	</div>
</div>

<style>
	.updating-database-popup {
		position: fixed;
		top: 40%;
		left: 50%;
		transform: translate(-50%, -50%);
		padding: 20px;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		box-shadow: var(--box-shadow);
		z-index: 100;
		text-align: center;
		border-radius: 8px;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.spinner-border {
		height: 100px;
		width: 100px;
		/* border-width: 0.7rem; */
	}
</style>
