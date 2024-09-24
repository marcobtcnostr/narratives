<!-- src\lib\components\modals\NarrativesDatabaseAddWindow.svelte -->
<script lang="ts">
	import { slide } from 'svelte/transition';
	import { writable } from 'svelte/store';
	import { addContentId } from '$lib/api/narratives-api'; // Adjust the path as necessary

	let contentText = writable(''); // Store for the input text value

	// Function triggered on button click
	async function addContent() {
		const contentId = $contentText; // Get current content text
		try {
			await addContentId(contentId); // Call the API function
			contentText.set(''); // Clear the input field after successful addition
		} catch (error) {
			console.error('Failed to add content ID:', error);
			// Optionally handle the error, e.g., show an error message to the user
		}
	}
</script>

<div class="filter-window" in:slide={{ duration: 300 }}>
	<div class="input-container">
		<input type="text" bind:value={$contentText} placeholder="Enter content here..." />
		<button on:click={addContent}>Add</button>
	</div>
</div>

<style>
	.filter-window {
		color: black;
		position: absolute;
		left: 80px;
		right: 80px;
		background-color: var(--navbar-bg-color);
		z-index: 10;
		box-shadow: var(--box-shadow);
		padding: 20px;
		display: flex;
		flex-direction: column;
		align-items: center;
		transition: transform 0.3s ease-out;
		flex-grow: 1;
	}

	.input-container {
		display: flex;
		align-items: center;
		gap: 10px; /* Adjust the space between the input and the button */
	}

	input[type='text'] {
		padding: 5px 10px;
		border: 1px solid #ccc;
		border-radius: 5px;
		font-size: 16px;
		width: 500px;
	}

	button {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
	}
</style>
