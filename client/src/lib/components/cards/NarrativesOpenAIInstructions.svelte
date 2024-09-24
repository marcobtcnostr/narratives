<!-- src\lib\components\cards\NarrativesOpenAIInstructions.svelte -->

<script lang="ts">
	import { narrativesStore } from '$lib/stores/narratives-stores';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
    import { loadContentForOpenAIChatbot } from '$lib/api/narratives-api';

	$: narratives = $narrativesStore; // Reactive subscription to narrativesStore
	$: if (narratives) {
		// console.log('Updated narratives:', narratives);
	}

	// Function to load content IDs into the chatbot
	async function loadContentIDs() {
		const narratives = get(narrativesStore); // Get the current value of the narrativesStore
		const contentIDs = narratives.map((narrative) => narrative.content_id); // Assuming each narrative has a 'content_id'
		try {
			await loadContentForOpenAIChatbot(contentIDs);
			console.log('Content IDs loaded successfully');
		} catch (error) {
			console.error('Error loading content IDs:', error);
		}
	}
</script>

<main class="container">
    <div class="button-container">
        <button on:click={loadContentIDs}>Load Content for Chatbot</button>
    </div>
    <div class="text-container">
        <p>You are a helpful assistant.</p>
    </div>
</main>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center; /* Centers children (button and text-container) horizontally */
    }

    .button-container {
        margin-top: 20px; /* Adjust as needed for spacing */
        width: 100%; /* Full width to center button correctly */
        display: flex;
        justify-content: center; /* Centers the button horizontally */
    }

    button {
        background-color: var(--button-bg-color);
        box-shadow: var(--box-shadow);
        color: var(--button-text-color);
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
        cursor: pointer;
        /* Additional button styles */
    }

    .text-container {
        /* Styles for the text container, if needed */
        margin-top: 20px; /* Adjust as needed for spacing */
    }
</style>
