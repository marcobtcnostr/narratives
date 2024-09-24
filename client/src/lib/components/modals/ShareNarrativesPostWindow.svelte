<!-- src\lib\components\modals\ShareNarrativesPostWindow.svelte -->
<script lang="ts">
    import { onMount } from 'svelte';
    import { writable, get } from 'svelte/store';
    import { currentUser, ndk } from '$lib/stores/social-stores';
    import { createEventDispatcher } from 'svelte';
    import Avatar from '$lib/components/user/Avatar.svelte';
    import Name from '$lib/components/user/Name.svelte';
    import SendIcon from '$lib/components/icons/SendIcon.svelte';
    import { NDKEvent } from '@nostr-dev-kit/ndk';
    import { narrativesStore } from '$lib/stores/narratives-stores';
    
    const dispatch = createEventDispatcher();
    let newPostContent = writable('');

    // Function to create a kind 9998 event for each narrative
    async function postNarrativesAsKind9998() {
        const narratives = get(narrativesStore);
        const postedEventIds = [];

        for (const narrative of narratives) {
            const eventDetails = {
                kind: 9998, // Event kind for narrative
                content: narrative.summary, // Narrative content
                pubkey: get(currentUser).pubkey,
                created_at: Math.floor(Date.now() / 1000),
                tags: [
                    ['content_id', narrative.content_id],
                    ['title', narrative.title],
                    ['publisher', narrative.publisher],
                    ['author', narrative.author || ''],
                    ['date_published', narrative.date_published || ''],
                    ['date_added', narrative.date_added || ''],
                    ['duration', narrative.duration.toString() || ''],
                    ['platform', narrative.platform || ''],
                    ['transcript', ''],
                    ['summary', narrative.summary || ''],
                    ['sentiment_analysis', narrative.sentiment_analysis.toString() || ''],
                    ['macro_topic', narrative.macro_topic || ''],
                    ['publisher_political_orientation', narrative.publisher_political_orientation || ''],
                    ['country', narrative.country || ''],
                    ['sent_by', narrative.sent_by || ''],
                    ['comments', narrative.comments || ''],
                    ['reference_image', narrative.reference_image || '']
                ]
            };

            const ndkEvent = new NDKEvent(get(ndk), eventDetails);

            try {
                await ndkEvent.publish();
                console.log(`Posted kind 9998 event for narrative: ${narrative.title}`);
                console.log('Kind 9998 Event Details:', ndkEvent);
                postedEventIds.push(ndkEvent.id); // Store the event ID for reference
            } catch (error) {
                console.error('Error posting kind 9998 event:', error);
            }
        }

        return postedEventIds;
    }

    // Function to create a kind 9999 event that references the kind 9998 events
    async function createKind9999Event(postedEventIds, postContent) {
        if (!postedEventIds.length) {
            console.log('No kind 9998 events to reference.');
            return;
        }

        const eventDetails = {
            kind: 9999, // Event kind 9999
            content: postContent, // Use the user input from newPostContent as the content
            pubkey: get(currentUser).pubkey,
            created_at: Math.floor(Date.now() / 1000),
            tags: postedEventIds.map((id) => ['e', id]) // Use the kind 9998 event IDs as tags
        };

        const ndkEvent = new NDKEvent(get(ndk), eventDetails);

        try {
            await ndkEvent.publish();
            console.log('Successfully posted kind 9999 event with user input and references to kind 9998 events');
            console.log('Kind 9999 Event Details:', ndkEvent);
        } catch (error) {
            console.error('Error posting kind 9999 event:', error);
        }
    }

    async function handlePost() {
        const postContent = $newPostContent.trim();
        if (postContent === '') {
            console.error('Post content cannot be empty');
            return;
        }

        // Post narratives as kind 9998 events
        const postedEventIds = await postNarrativesAsKind9998();

        // Create a kind 9999 event with user input content, referencing the kind 9998 events
        await createKind9999Event(postedEventIds, postContent);

        newPostContent.set(''); // Clear the input after posting
        dispatch('close'); // Optionally close the modal after posting
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
            <Avatar {ndk} user={$currentUser} class="event-card-avatar" />
            <Name {ndk} user={$currentUser} />
        </div>
    </div>

    <div class="event-card--content">
        <div class="textarea-wrapper">
            <textarea
                bind:this={textarea}
                bind:value={$newPostContent}
                on:input={autoResize}
                placeholder="Share your post here..."
            />
            <button on:click={handlePost} class="send-button rounded-icon">
                <SendIcon />
            </button>
        </div>
    </div>
</div>

<style>
    .textarea-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
    }

    textarea {
        background-color: var(--event-card-bg-color);
        color: var(--text-color);
        border: 1px solid var(--separator-line-color);
        border-radius: 0.5rem;
        padding: 1rem;
        min-height: 50px;
        max-height: 250px;
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
    }

    .send-button:hover {
        background-color: var(--text-color);
        color: var(--text-color-hover);
    }
</style>
