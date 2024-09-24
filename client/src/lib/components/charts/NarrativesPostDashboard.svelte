<!-- src\lib\components\charts\NarrativesPostDashboard.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import GenericCarousel from '$lib/components/carousel/GenericCarousel.svelte';
	import NarrativesStackedBars from '$lib/components/charts/NarrativesStackedBars.svelte';
	import NarrativesDurationBars from '$lib/components/charts/NarrativesDurationBars.svelte';
	import NarrativesCountryBars from '$lib/components/charts/NarrativesCountryBars.svelte';
	import NarrativesWorldMap from '$lib/components/charts/NarrativesWorldMap.svelte';
	import NarrativesTopicBars from '$lib/components/charts/NarrativesTopicBars.svelte';
	import NarrativesPublisherPoliticalOrientation from '$lib/components/charts/NarrativesPublisherPoliticalOrientation.svelte';
	import SplitInThreeWindows from '$lib/components/draggable/SplitInThreeWindows.svelte';
	import SplitInTwoWindows from '$lib/components/draggable/SplitInTwoWindows.svelte';
	import { ndk } from '$lib/stores/social-stores';
	import { narrativesPostStore } from '$lib/stores/narratives-stores';

	export let event; // This is the kind 9999 event

	// Dynamically updating store to hold kind 9998 posts
	let narrativesPostStoreLocal = writable([]);

	// Fetch kind 9998 events referenced by kind 9999
	async function fetchReferencedEvents() {
		const referencedIds = event.tags.filter((tag) => tag[0] === 'e').map((tag) => tag[1]);
		const referencedEvents = [];

		for (const id of referencedIds) {
			try {
				const fetchedEvent = await $ndk.fetchEvent(id); // Fetch each kind 9998 event

				// console.log('fetchedEvent:', fetchedEvent);

				if (fetchedEvent) {
					referencedEvents.push(fetchedEvent);
				}
			} catch (error) {
				console.error(`Error fetching kind 9998 event with id ${id}:`, error);
			}
		}

		// Update narrativesPostStore with fetched kind 9998 events
		narrativesPostStoreLocal.set(
			referencedEvents.map((ev) => {
				const getTagValue = (tagName) => {
					const tag = ev.tags.find((tag) => tag[0] === tagName);
					return tag ? tag[1] : null;
				};

				return {
					content_id: getTagValue('content_id'),
					title: getTagValue('title'),
					publisher: getTagValue('publisher'),
					author: getTagValue('author'),
					date_published: getTagValue('date_published'),
					date_added: getTagValue('date_added'),
					duration: parseInt(getTagValue('duration') || '0', 10),
					platform: getTagValue('platform'),
					transcript: getTagValue('transcript'),
					summary: getTagValue('summary'),
					sentiment_analysis: parseInt(getTagValue('sentiment_analysis') || '0', 10),
					macro_topic: getTagValue('macro_topic'),
					publisher_political_orientation: getTagValue('publisher_political_orientation'),
					country: getTagValue('country'),
					sent_by: getTagValue('sent_by'),
					comments: getTagValue('comments'),
					reference_image: getTagValue('reference_image')
				};
			})
		);
	}

	onMount(fetchReferencedEvents); // Fetch referenced events when the component mounts

	// Carousel components
	let images = [];

	let components = [
		{ id: 1, type: 'component', component: NarrativesCountryBars },
		{ id: 2, type: 'component', component: NarrativesWorldMap },
		{ id: 3, type: 'component', component: NarrativesPublisherPoliticalOrientation },
		{ id: 4, type: 'component', component: NarrativesDurationBars },
		{ id: 5, type: 'component', component: NarrativesTopicBars }
	];
</script>

<div class="flex flex-col overflow">
	<!-- Pass the store to the carousel and other components -->
	<div style="box-shadow: var(--box-shadow);">
		<GenericCarousel {images} {components} dataStore={narrativesPostStoreLocal} />
	</div>

	<div style="box-shadow: var(--box-shadow);">
		<SplitInThreeWindows {images} {components} dataStore={narrativesPostStoreLocal} />
	</div>

	<!-- <div style="box-shadow: var(--box-shadow);">
		<SplitInTwoWindows {images} {components} dataStore={narrativesPostStoreLocal} />
	</div> -->
</div>

<style>
	/* Styles */
</style>
