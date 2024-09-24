<!-- src\lib\components\actions\Reply.svelte -->

<script lang="ts">
	import { currentUser, ndk } from '$lib/stores/social-stores';
	import { NDKEvent } from '@nostr-dev-kit/ndk';
	import SendIcon from '$lib/components/icons/SendIcon.svelte';
	export let event;
	let message = '';
	let textarea;

	function resizeTextarea() {
		textarea.style.height = 'auto';
		textarea.style.height = `${textarea.scrollHeight}px`;
	}

	async function handleReply() {
		if (message.trim() === '') {
			console.log('Message content cannot be empty');
			return;
		}

		// console.log('event:', event)

		const replyDetails = {
			kind: 1,
			content: message.trim(),
			pubkey: currentUser.pubkey,
			created_at: Math.floor(Date.now() / 1000),
			tags: [
				['e', event.id, '', 'reply'],
				['p', event.pubkey]
			]
		};

		const replyEvent = new NDKEvent($ndk, replyDetails);

		try {
			await replyEvent.publish();
			message = '';  // Clear the message
			resizeTextarea();  // Reset textarea height after message is sent
		} catch (error) {
			console.error('Error posting reply:', error);
		}
	}
</script>

<div class="reply-card">
	<div class="textarea-wrapper">
		<textarea bind:this={textarea} bind:value={message} on:input={resizeTextarea} placeholder="Write your reply..."></textarea>
		<button on:click={handleReply} class="send-button rounded-icon">
			<SendIcon />
		</button>
	</div>
</div>


<style>
	.reply-card {
		@apply rounded-lg transition-all duration-300 ease-in-out;
		display: flex;
		flex-direction: column;
		opacity: 1;
		transition: opacity 0.3s ease-in-out;
		color: var(--text-color);
		margin-bottom: 10px;
		padding-top: 0.5rem;
		padding-bottom: 0.5rem;
		padding-left: 1.5rem;
		cursor: pointer;
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
        min-height: 50px; /* Adjust based on your UI needs */
        max-height: 250px;
		overflow-y: auto;
        outline: none;
        width: 100%;
		resize: none;

		&:hover {
			@apply bg-opacity-90;
			box-shadow: 0 0 0 0.125rem var(--button-active-border-color, var(--logo-color));
		}
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
