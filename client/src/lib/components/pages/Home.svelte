<!-- src\lib\components\pages\Home.svelte -->
<script lang="ts">
	import DefaultFeed from '$lib/components/feed/DefaultFeed.svelte';
	import EventThreadWindow from '$lib/components/modals/EventThreadWindow.svelte';
	import { NDKEvent } from '@nostr-dev-kit/ndk';
	import { currentUser, userFollows, ndk } from '$lib/stores/social-stores';

	let showThread = false;
	export let event = null;

	function openEventThread(eventDetail) {
		event = eventDetail.detail.event;
		showThread = true;
		console.log('event', eventDetail.detail.event);
	}

	function closeEventThread() {
		showThread = false;
		event = null;
	}
</script>

<div class="home-container {showThread ? 'dimmed' : ''}">
	<DefaultFeed on:openThread={openEventThread} />

	{#if showThread}
		<EventThreadWindow ndk={$ndk} {event} on:closeThread={closeEventThread} />
	{/if}
</div>

<style lang="postcss">
	.home-container {
		background-color: none;
		padding: 15px;
		min-height: 100vh;
	}

	@media (max-width: 390px) {
		.home-container {
			background-color: none;
			padding: 5px;
			min-height: 100vh;
		}
	}

	.dimmed::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
		z-index: 100; /* Ensure it's high enough to cover the content but lower than the modal */
	}
</style>
