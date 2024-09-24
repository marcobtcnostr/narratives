<!-- src\lib\components\event\EventThread.svelte -->

<script lang="ts">
	import { NDKSubscriptionCacheUsage } from '@nostr-dev-kit/ndk';
	import { fade } from 'svelte/transition';
	import { SvelteComponent, onDestroy } from 'svelte';
	import EventCard from '$lib/components/event/EventCard.svelte';
	import ElementConnector from '$lib/components/event/ElementConnector.svelte';

	export let ndk;
	export let event;
	export let skipEvent = false;
	export let eventComponent = EventCard;
	export let eventComponentProps = {};
	export let whitelistPubkeys = undefined;
	export let useWhitelist = false;
	export let extraItemsFetcher = undefined;

	// Event IDs that are part of the thread
	let threadIds = new Map();
	let replyIds = new Map();
	let eventsByAuthor = new Set([event.id]);
	threadIds.set(event.id, event);
	/**
	 * Extra events are events that might be coming from alternative sources
	 * instead of coming from a relay
	 */
	let extraItems;
	if (extraItemsFetcher) {
		extraItems = extraItemsFetcher(event);
	}

	export let replies = ndk.storeSubscribe(
		{
			kinds: [1],
			'#e': Array.from(threadIds.keys())
		},
		{ closeOnEose: false, groupableDelay: 100, cacheUsage: NDKSubscriptionCacheUsage.ONLY_RELAY }
	);


	$: {

		const threadIdCountBefore = threadIds.size;
		const replyIdCountBefore = replyIds.size;

		// Update eventsByAuthor
		for (const taggedEvent of $replies) {
			if (taggedEvent.pubkey === event.pubkey) eventsByAuthor.add(taggedEvent.id);
		}

		// Find threaded events and replies
		for (const taggedEvent of $replies) {
			if (eventIsPartOfThread(taggedEvent)) threadIds.set(taggedEvent.id, taggedEvent);
		}

		for (const taggedEvent of $replies) {
			if (threadIds.has(taggedEvent.id)) continue;
			if (eventIsReply(taggedEvent)) replyIds.set(taggedEvent.id, taggedEvent);
		}

		// Do we need to redo our filter?
		if (threadIdCountBefore < threadIds.size) {
			replies.unsubscribe();
			replies = ndk.storeSubscribe(
				{
					kinds: [1],
					'#e': Array.from(threadIds.keys())
				},
				{ closeOnEose: false, groupableDelay: 100, subId: 'thread-filter' }
			);
			threadIds = threadIds;
		}
        
		if (replyIdCountBefore < replyIds.size) {
			replyIds = replyIds;
		}
	}

	function eventIsPartOfThread(e) {
		// must be same author
		if (event.pubkey !== e.pubkey) return false;
		// Check if all tagged events are by the original author
		const taggedEventIds = e.getMatchingTags('e').map((tag) => tag[1]);
		// const allTaggedEventsAreByOriginalAuthor = taggedEventIds.every((id) => eventsByAuthor.has(id));

		const allTaggedEventsAreByOriginalAuthor = false
		// console.log('allTaggedEventsAreByOriginalAuthor', allTaggedEventsAreByOriginalAuthor)

		return allTaggedEventsAreByOriginalAuthor;
	}

	function eventIsReply(event) {
        // console.log('isReply(event)', isReply(event))
		return isReply(event);
	}

	onDestroy(() => {
		replies.unsubscribe();
	});

	function isReply(e) {
		const replyMarker = e.tags.find((tag) => {
			return threadIds.has(tag[1]) && tag[3] === 'reply';
		});
		if (replyMarker) return true;

		// check if the event has valid markers, if it does and we don't have an explicit reply, this was
		// probably a reply to a reply or a mention
		const hasMarker = !!e.tags.find((tag) => ['reply', 'mention'].includes(tag[3]));
		if (hasMarker) return false;

		// if we don't have markers, check if there are tags for other events that the main event
		// does not have
		const expectedTags = event.getMatchingTags('e').map((tag) => tag[1]);
		expectedTags.push(event.id);
		// return true if there are no unexpected e tags
		return e.getMatchingTags('e').every((tag) => expectedTags.includes(tag[1]));
	}

	function sortThread(a, b) {
		return b.created_at - a.created_at;
	}

	function sortReplies(a, b) {
		return b.created_at - a.created_at;
	}

	let eventContainer;
</script>

<div class="event-thread flex flex-col gap-1" transition:fade={{ duration: 500 }}>
	{#if !skipEvent}
		<div class="event-wrapper w-full join-vertical join" bind:this={eventContainer}>
			{#each Array.from(threadIds.values()).sort(sortThread) as event (event.id)}
				<svelte:component
					this={eventComponent}
					{event}
					...eventComponentProps
					class="{$$props.eventComponentClass ?? ''} w-full join-item"
				/>
			{/each}
		</div>
	{/if}

	{#if replyIds.size > 0 || $extraItems}
		<div class="event-thread--indent">
			{#each $extraItems ?? [] as item (item.props.key)}
				<ElementConnector from={eventContainer} topOffset={80}>
					<svelte:component this={item.component} {...item.props} />
				</ElementConnector>
			{/each}

			{#each Array.from(replyIds.values()).sort(sortReplies) as reply (reply.id)}
				{#if !whitelistPubkeys || !useWhitelist || whitelistPubkeys.has(reply.pubkey)}
					<ElementConnector from={eventContainer} topOffset={80}>
						<svelte:self
							{ndk}
							event={reply}
							on:reply
							skipEvent={false}
							{eventComponent}
							{eventComponentProps}
							{whitelistPubkeys}
							{useWhitelist}
							{extraItemsFetcher}
						/>
					</ElementConnector>
				{:else if whitelistPubkeys && useWhitelist && !whitelistPubkeys.has(reply.pubkey)}
					<div class="flex flex-col gap-4">
						<div class="flex flex-row gap-2 items-center">
							<span class="text-base-content flex-grow ui-common-font-light"
								>This reply was hidden</span
							>
							<button
								class="btn btn-sm bg-base-300 capitalize"
								on:click={() => (useWhitelist = false)}>Show anyway</button
							>
						</div>
					</div>
				{/if}
			{/each}
		</div>
	{/if}
</div>

<style>
	.event-thread--indent {
		padding-left: 30px;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		margin-top: 1rem;
		z-index: 1000 !important;
	}
</style>
