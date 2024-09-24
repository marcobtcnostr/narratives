<!-- src\lib\components\cards\NarrativesOpenAIChatbot.svelte -->

<script lang="ts">
	import { narrativesStore } from '$lib/stores/narratives-stores';
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

    import { chatWithOpenAIAssistant, closeOpenAIChat } from '$lib/api/narratives-api';


	let message = '';
	let chatMessages = writable([]);

	// Function to send message to the chatbot
	async function sendOpenAiChatbotMessage() {
		try {
            const botResponse = await chatWithOpenAIAssistant(message);
            chatMessages.update(messages => [
                ...messages,
                { type: 'user', text: message },
                { type: 'bot', text: botResponse }
            ]);
            message = ''; // Clear input after sending
        } catch (error) {
            console.error('Failed to send message to chatbot:', error);
        }
	}

	// Example function to close the chat (you might call this when unmounting the component or through a UI action)
	async function closeOpenAiChatbotChat() {
		try {
            await closeOpenAIChat();
            console.log('Chat closed successfully');
        } catch (error) {
            console.error('Failed to close chat:', error);
        }
	}
</script>

<main>
	<div class="chat-container">
		<div class="messages">
			{#each $chatMessages as chatMessage (chatMessage)}
				<div class="message {chatMessage.type}">
					{chatMessage.text}
				</div>
			{/each}
		</div>
		<div class="input-area">
			<input
				bind:value={message}
				on:keydown={(e) => e.key === 'Enter' && sendOpenAiChatbotMessage()}
				placeholder="Type a message..."
			/>
			<button on:click={sendOpenAiChatbotMessage}>Send</button>
		</div>
	</div>
</main>

<style>
	.chat-container {
		display: flex;
		flex-direction: column;
		height: 350px;
		max-height: 1000px;
		/* border: 1px solid #ccc; */
		/* border-radius: 8px; */
		overflow: hidden;
        width: 100%; /* Ensure the container is full width */
		box-sizing: border-box;
	}

	.messages {
		flex-grow: 1;
		overflow-y: auto;
		padding: 10px;
		/* background-color: #f0f0f0; */
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.message {
        margin: 0; /* Remove default paragraph margin */
        padding: 0; /* If you don't want any padding within the paragraph itself */
		max-width: 80%;
		line-height: 1.4;
		padding: 10px;
		border-radius: 8px;
		position: relative;
		font-size: 16px;
        /* white-space: pre-wrap;  */
        word-break: break-word; 
	}

	.user {
		align-self: flex-end;
		background-color: #007aff;
		color: white;
	}

	.bot {
		align-self: flex-start;
		background-color: var(--button-hover-bg-color);
        color: var(--button-hover-text-color);
		border: 1px solid #ccc;
	}

	.input-area {
		display: flex;
		padding: 10px;
		/* background-color: #fff; */
		/* border-top: 1px solid #ccc; */
	}

	.input-area input {
		flex-grow: 1;
		padding: 10px;
		margin-right: 10px;
		font-size: 16px;
		border-radius: 8px;
		border: 1px solid #ccc;
	}

	.input-area button {
		padding: 10px 20px;
		font-size: 16px;
		border-radius: 8px;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		border: none;
		cursor: pointer;
	}

	.input-area button:hover {
		background-color: var(--button-hover-bg-color);
        color: var(--button-hover-text-color);
	}
</style>
