<!-- src\lib\components\event\content\Kind9999.svelte -->

<script lang="ts">
	import {
		parseContent,
		truncateContent,
		LINK,
		NEWLINE,
		TOPIC,
		LINKCOLLECTION,
		groupContent
	} from '$lib/utils/kind-utils';

	import { pluck, values, without } from 'ramda';

	import EventCard from '$lib/components/event/EventCard.svelte';
	import NoteContentNewline from '$lib/components/event/content/NoteContentNewline.svelte';
    import NoteContentLink from '$lib/components/event/content/NoteContentLink.svelte';
    import NoteContentTopic from '$lib/components/event/content/NoteContentTopic.svelte';
    import NoteContentPerson from '$lib/components/event/content/NoteContentPerson.svelte';

    import NarrativesPostDashboard from '$lib/components/charts/NarrativesPostDashboard.svelte';

	export let event;
	export let maxLength;
	export let ndk;
	export let anchorId = null;
	export let showEntire = false;
	export let showMedia = true;
	export let content = event.content;
	export let mediaCollectionComponent = undefined;

	export let eventCardComponent = EventCard;

	export const getLinks = (parts) =>
		pluck(
			'value',
			parts.filter((x) => x.type === LINK && x.isMedia)
		);

	const fullContent = parseContent({ ...event, content });
	const shortContent = truncateContent(fullContent, { maxLength, showEntire, showMedia });
	const groupedContent = groupContent(shortContent);
	const links = getLinks(shortContent);

	export const isNewline = (i) => !shortContent[i] || shortContent[i].type === NEWLINE;
	export const isStartOrEnd = (i) => isNewline(i - 1) || isNewline(i + 1);
</script>

<!-- {content} -->

<div class="event-content flex flex-col gap-2 overflow-hidden text-ellipsis {$$props.class??""}">
    <p>
        {#each groupedContent as { type, value }, i}
            {#if type === NEWLINE}
                <NoteContentNewline {value} />
            {:else if type === TOPIC}
                <NoteContentTopic {value} />
            {:else if type === LINK}
                <NoteContentLink {value} {showMedia} />
            {:else if type === LINKCOLLECTION}
                {#if mediaCollectionComponent}
                    <svelte:component this={mediaCollectionComponent} links={value.map(v=>v.value.url)} />
                {:else}
                    <div class="note-media--wrapper">
                        {#each value as {type: _type, value: _value}, j}
                            <NoteContentLink value={_value} {showMedia} />
                        {/each}
                    </div>
                {/if}
            {:else if type.match(/^nostr:np(rofile|ub)$/)}
                <NoteContentPerson {ndk} {value} on:click />
            {:else if type.startsWith('nostr:') && showMedia && isStartOrEnd(i) && value.id !== anchorId}
                <svelte:component this={eventCardComponent} {ndk} id={value.id} relays={value.relays} />
            {:else if type.startsWith('nostr:')}
                <svelte:component this={eventCardComponent} {ndk} id={value.id} relays={value.relays} />
            {:else}
                {value}
            {/if}
            {' '}
        {/each}
    </p>

    <div>
        <NarrativesPostDashboard {event}/>
    </div>


    <!-- {#if showMedia && extraLinks.length > 0}
        <MediaSet links={extraLinks} />
    {/if} -->
</div>

