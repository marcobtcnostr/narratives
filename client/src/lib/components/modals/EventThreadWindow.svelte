<!-- src\lib\components\modals\EventThreadWindow.svelte -->

<script lang="ts">
	import { fly } from 'svelte/transition';
	import { NDKEvent } from '@nostr-dev-kit/ndk';
	import { createEventDispatcher } from 'svelte';
	import EventThread from '$lib/components/event/EventThread.svelte';

	import XIcon from '$lib/components/icons/XIcon.svelte';

	export let event;
	export let ndk;

	const dispatch = createEventDispatcher();

	function closeThread() {
		dispatch('closeThread');
	}
</script>


<button class="close-button" on:click={closeThread} aria-label="Close" in:fly={{ y: 500, duration: 200 }}>
	<XIcon />
</button>

<div class="event-thread-window fixed" in:fly={{ y: 500, duration: 200 }}>
	<EventThread ndk={ndk} {event} />
</div>

<style lang="postcss">
	.event-thread-window {
		background: var(--bg-color);
		z-index: 999;
		width: 100%;
		min-height: 80vh;
		max-height: 80vh;
		border: 1px solid var(--separator-line-color);
		border-top-left-radius: 1rem;
		border-top-right-radius: 1rem;
		overflow-y: scroll;
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		padding-left: 15px;
		padding-right: 15px;
		padding-bottom: 50px;
	}

	.close-button {
		@apply w-6 h-6 xs:w-6 xs:h-6 sm:w-8 sm:h-8 md:w-8 md:h-8 lg:w-12 lg:h-12;
    	border: none;
		z-index: 1000;
        position: absolute;
        bottom: 81vh;
        left: 50%; 
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        justify-content: center;
        background: red;
		color: white;
        border-radius: 50%;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        cursor: pointer;
    }
</style>
