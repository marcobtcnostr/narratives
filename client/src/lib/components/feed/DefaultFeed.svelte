<!-- src\lib\components\feed\DefaultFeed.svelte -->
<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { writable } from 'svelte/store';
	import { currentUser, userFollows, ndk } from '$lib/stores/social-stores';
	import { NDKEvent, NDKSubscriptionCacheUsage } from '@nostr-dev-kit/ndk';
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';
	import Avatar from '$lib/components/user/Avatar.svelte';
	import Name from '$lib/components/user/Name.svelte';
	import SendIcon from '$lib/components/icons/SendIcon.svelte';

	import EventCard from '$lib/components/event/EventCard.svelte';

	let events = writable<NDKEvent[]>([]);
	const authors = Array.from($userFollows).map((user) => user.pubkey);
	let eventCount = 100; // Start with 10 events

	const filters = {
		authors: authors,
		kinds: [1, 9998, 9999],
		limit: eventCount
	};

	let feedSubscription;

	function loadMoreEvents() {
		eventCount += 10; // Load 10 more events each time
		filters.limit = eventCount;
		console.log('eventCount', eventCount);
		updateSubscription(); // Update the subscription with new limit
	}

	function updateSubscription() {
		if (feedSubscription) {
			feedSubscription.unsubscribe(); // Unsubscribe if already subscribed
		}
		feedSubscription = $ndk.storeSubscribe(filters, {
			subId: 'feed',
			cacheUsage: NDKSubscriptionCacheUsage.PARALLEL,
			groupable: true,
    		groupableDelay: 500,
		});

		// feedSubscription.subscribe((newEvents) => {
		// 	events.set(
		// 		newEvents
		// 			.filter((event) => !event.tags.some((tag) => tag[0] === 'e'))
		// 			.sort((a, b) => b.created_at - a.created_at)
		// 	);
		// });

		feedSubscription.subscribe((newEvents) => {
			events.set(
				newEvents
					.filter((event) => {
						// Keep all kind 9998 events
						if (event.kind === 9998) return true;
						// Keep all kind 9999 events
						if (event.kind === 9999) return true;
						// Filter out kind 1 events with an 'e' tag
						if (event.kind === 1 && event.tags.some((tag) => tag[0] === 'e')) return false;
						// Otherwise, keep the event
						return true;
					})
					.sort((a, b) => b.created_at - a.created_at) // Sort events in descending order
			);
		});
	}

	onMount(() => {
		updateSubscription(); // Initial subscription setup
		return () => {
			feedSubscription.unsubscribe();
		};
	});

	const dispatch = createEventDispatcher();

	function openEventThread(event) {
		dispatch('openThread', { event });
	}

	let newPostContent = '';

	async function handlePost() {
		// const postedEventId = [];

		if (newPostContent.trim() === '') {
			console.error('Post content cannot be empty');
			return;
		}
		const eventDetails = {
			kind: 1,
			content: newPostContent.trim(),
			pubkey: $currentUser.pubkey,
			created_at: Math.floor(Date.now() / 1000),
			tags: []
		};
		const ndkEvent = new NDKEvent($ndk, eventDetails);
		try {
			await ndkEvent.publish();
			console.log('Successfully posted:', newPostContent);
			newPostContent = '';
			// postedEventId.push(ndkEvent.id);
			// console.log('postedEventId:', postedEventId);
		} catch (error) {
			console.error('Error posting event:', error);
		}
	}

	let textarea;

	onMount(() => {
		textarea.style.height = 'auto';
		textarea.style.height = textarea.scrollHeight + 'px';
	});

	function autoResize() {
		textarea.style.height = 'auto';
		textarea.style.height = textarea.scrollHeight + 'px';
	}
</script>

<div class="event-card">
	<div class="event-card--header">
		<div class="flex items-center space-x-4">
			<Avatar {ndk} user={$currentUser} />
			<Name {ndk} user={$currentUser} />
		</div>
	</div>

	<div class="textarea-wrapper">
		<textarea
			bind:this={textarea}
			bind:value={newPostContent}
			on:input={autoResize}
			placeholder="What's on your mind?"
		/>
		<button on:click={handlePost} class="send-button rounded-icon">
			<SendIcon />
		</button>
	</div>
</div>

<div class="feed-container">
	{#each $events as event (event.id)}
		{#if event.kind !== 9998}
			<div in:fade>
				<EventCard ndk={$ndk} {event} on:openThread={() => openEventThread(event)} />
			</div>
		{/if}
	{/each}
</div>

<button on:click={loadMoreEvents} class="load-more">Load More</button>

<style lang="postcss">
	.feed-container {
		min-height: 100vh;
	}

	.load-more {
		margin: 20px auto;
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
		cursor: pointer;
		display: block;
		margin-bottom: 50px;
	}

	.textarea-wrapper {
		position: relative;
		display: flex;
		align-items: center;
	}

	textarea {
		background-color: var(--event-card-bg-color);
		color: var(--color-text);
		border: 1px solid var(--separator-line-color);
		border-radius: 0.5rem;
		padding: 1rem;
		min-height: 50px; /* Initial minimum height */
		max-height: 250px; /* Maximum height before scrolling */
		overflow-y: auto;
		outline: none;
		width: 100%;
		resize: none;
	}

	textarea::placeholder {
		color: var(--color-text);
		opacity: 1;
	}

	.send-button {
		position: absolute;
		right: 0.5rem;
		bottom: 0.5rem;
		cursor: pointer;
		color: var(--text-color);
		padding: 0.5rem;
		cursor: pointer;
	}

	.send-button:hover {
		background-color: var(--text-color);
		color: var(--text-color-hover);
	}
</style>
