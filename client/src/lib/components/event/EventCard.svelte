<!-- src\lib\components\event\EventCard.svelte -->

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { NDKEvent } from '@nostr-dev-kit/ndk';
	import { createEventDispatcher } from 'svelte';
	import { writable } from 'svelte/store';

	import Avatar from '$lib/components/user/Avatar.svelte';
	import Name from '$lib/components/user/Name.svelte';
	import Time from 'svelte-time';
	import EventCardDropdownMenu from '$lib/components/event/EventCardDropdownMenu.svelte';
	import EventContent from '$lib/components/event/content/EventContent.svelte';
	import Reply from '$lib/components/actions/Reply.svelte';
	import ChatIcon from '$lib/components/icons/ChatIcon.svelte';
	import ReplyIcon from '$lib/components/icons/ReplyIcon.svelte';
	import ArrowRepeatIcon from '$lib/components/icons/ArrowRepeatIcon.svelte';
	import LightningChargeIcon from '$lib/components/icons/LightningChargeIcon.svelte';

	export let relativeTimeAllowed = true;
	export let event = undefined;
	export let ndk;
	export let id = undefined;
	export const relays = undefined;

	const eventPromise = new Promise(async (resolve, reject) => {
		if (event) {
			resolve(event);
		} else if (id) {
			event = await ndk.fetchEvent(id);
			if (!event) reject('Event not found');
			else resolve(event);
		}
		// console.log('event author', event.author)
		// console.log('event content', event.content)
	});

	let showReply = writable(false);

	function toggleReply() {
		showReply.update((value) => !value);
	}

	const dispatch = createEventDispatcher();

	function openEventThread() {
		dispatch('openThread', { event });
		console.log('EventCard openThread', event);
	}

	export let timeAgoCutoff = 60 * 60 * 24;
	function useRelativeTime() {
		if (!relativeTimeAllowed || !event) return false;
		const now = Date.now();
		const diff = now - event.created_at * 1000;
		return diff < 1000 * timeAgoCutoff;
	}
</script>

{#await eventPromise then}
	<div class="event-card">
		<div class="event-card--header">
			<div class="flex items-center space-x-4">
				<Avatar {ndk} user={event?.author} />
				<Name {ndk} user={event?.author} />
			</div>
			<div class="flex items-center space-x-2">
				<Time relative={useRelativeTime()} live={true} timestamp={event?.created_at * 1000} />
				<EventCardDropdownMenu {event} />
			</div>
		</div>

		{#if !$$slots.default}
			<div class="event-card--content">
				<EventContent {ndk} {event} />
			</div>
		{:else}
			<slot />
		{/if}

		<div class="reaction-toolbar">
			<button class="rounded-icon reaction-icon" on:click={toggleReply}
				><ReplyIcon /></button
			>
			<button class="rounded-icon reaction-icon" on:click={openEventThread}
				><ChatIcon /></button
			>
			<button class="rounded-icon reaction-icon" on:click={toggleReply}
				><ArrowRepeatIcon /></button
			>
			<button class="rounded-icon reaction-icon" on:click={toggleReply}
				><LightningChargeIcon /></button
			>
		</div>
	</div>

	<div class="reply-container">
		{#if $showReply}
			<Reply {ndk} {event} />
		{/if}
	</div>
{:catch error}
	<div class="event-card">
		<p class="event-card--error">{error}</p>
	</div>
{/await}

<style lang="postcss">
	.reaction-toolbar {
		display: flex;
		align-items: center;
		justify-content: flex-end;
		gap: 1rem;
		width: 100%;
		cursor: pointer;
	}

	.reaction-icon {
		color: var(--text-color);
		border: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		padding: 0.5rem;
	}

	.reaction-icon:hover {
        background-color: var(--text-color);
        color: var(--text-color-hover);
    }
</style>
