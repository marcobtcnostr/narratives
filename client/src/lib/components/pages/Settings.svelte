<!-- src\lib\components\pages\Settings.svelte -->
<script lang="ts">
	import { writable } from 'svelte/store';

	import { serverUrl } from '$lib/stores/narratives-stores';

	import { clearCache } from '$lib/utils/social-utils';

	import ChevronRightIcon from '$lib/components/icons/ChevronRightIcon.svelte';
	import SunIcon from '$lib/components/icons/SunIcon.svelte';
	import MoonIcon from '$lib/components/icons/MoonIcon.svelte';
	import StarIcon from '$lib/components/icons/StarIcon.svelte';

	import { fetchApiKeys, updateApiKey } from '$lib/api/narratives-api';

	// Initialize the theme store with the value from localStorage or default to 'light'
	const storedTheme = localStorage.getItem('theme');
	let theme = writable(storedTheme || 'light');
	let selectedSetting = writable('');

	// Reactive statement to update the document's theme attribute and localStorage whenever the theme changes
	$: {
		document.documentElement.setAttribute('data-theme', $theme);
		localStorage.setItem('theme', $theme);
	}

	// Function to update the theme
	function setTheme(newTheme) {
		theme.set(newTheme);
		console.log('Theme changed to:', newTheme);
	}

	// Function to select setting
	function selectSetting(setting) {
		selectedSetting.set(setting);
	}

	async function handleClearCache() {
		await clearCache();
		console.log('Cache clearing initiated from the layout component.');
	}

	let apiKeys = writable<{ api: string; key: string }[]>([]);

	const loadApiKeys = async () => {
		try {
			const keys = await fetchApiKeys();
			apiKeys.set(keys);
		} catch (error) {
			console.error('Failed to load API keys', error);
		}
	};

	const saveApiKey = async (api: string, key: string) => {
		try {
			await updateApiKey(api, key);
			await loadApiKeys();
		} catch (error) {
			console.error('Failed to save API key', error);
		}
	};

	loadApiKeys();

	// Using session store directly for the value
	let serverUrlValue = ''; // Temporary variable to bind the input

	// Fetch the initial server URL from the store
	serverUrl.subscribe((value) => {
		serverUrlValue = value;
	});

	// Function to update the server URL
	function updateServerUrl() {
		serverUrl.set(serverUrlValue); // Update the store with the input value
		console.log('Server URL updated to:', serverUrlValue);
	}
</script>

<div class="flex h-screen">
	<div class="w-2/5 p-4 settings-list">
		<h3 class="text-xl font-bold mb-4">Settings</h3>
		<div class="space-y-2">
			<button
				on:click={() => selectSetting('Theme')}
				class="flex justify-between items-center w-full px-4 py-2 text-left border settings-item"
			>
				Theme
				<svg><ChevronRightIcon /></svg>
			</button>
			<button
				on:click={() => selectSetting('API Keys')}
				class="flex justify-between items-center w-full px-4 py-2 text-left border settings-item"
			>
				API Keys
				<svg><ChevronRightIcon /></svg>
			</button>
			<button
				on:click={() => selectSetting('Server')}
				class="flex justify-between items-center w-full px-4 py-2 text-left border settings-item"
			>
				Server
				<svg><ChevronRightIcon /></svg>
			</button>
			<button
				on:click={() => selectSetting('Clear Cache')}
				class="flex justify-between items-center w-full px-4 py-2 text-left border settings-item"
			>
				Clear Cache
				<svg><ChevronRightIcon /></svg>
			</button>
		</div>
	</div>

	<div class="w-3/5 p-4">
		<div class="mb-4">
			<h3 class="text-xl font-bold">{$selectedSetting} Settings</h3>
		</div>

		<div>
			{#if $selectedSetting === 'Theme'}
				<div class="flex justify-around items-center w-full">
					<div class="flex flex-col justify-around items-center">
						<h4 class="mb-2">Light</h4>
						<button
							on:click={() => setTheme('light')}
							class:active={$theme === 'light'}
							class="theme-icon p-2 xs:h-12 xs:w-12 sm:h-14 sm:w-14 md:h-16 md:w-16 lg:h-20 lg:w-20"
						>
							<SunIcon />
						</button>
					</div>
					<div class="flex flex-col justify-around items-center">
						<h4 class="mb-2">Dark</h4>
						<button
							on:click={() => setTheme('dark')}
							class:active={$theme === 'dark'}
							class="theme-icon p-2 xs:h-12 xs:w-12 sm:h-14 sm:w-14 md:h-16 md:w-16 lg:h-20 lg:w-20"
						>
							<MoonIcon />
						</button>
					</div>
					<div class="flex flex-col justify-around items-center">
						<h4 class="mb-2">Custom</h4>
						<button
							on:click={() => setTheme('custom')}
							class:active={$theme === 'custom'}
							class="theme-icon p-2 xs:h-12 xs:w-12 sm:h-14 sm:w-14 md:h-16 md:w-16 lg:h-20 lg:w-20"
						>
							<StarIcon />
						</button>
					</div>
				</div>
			{:else if $selectedSetting === 'API Keys'}
				<div class="api-keys-settings">
					{#each $apiKeys as key}
						<div class="api-key-item">
							<input type="text" bind:value={key.api} disabled class="api-key-input" />
							<input type="text" bind:value={key.key} class="api-key-input" />
							<button on:click={() => saveApiKey(key.api, key.key)} class="generic-button"
								>Update</button
							>
						</div>
					{/each}
				</div>
			{:else if $selectedSetting === 'Server'}
				<div class="server-settings">
					<label for="server-url">Server URL:</label>
					<input type="text" id="server-url" bind:value={serverUrlValue} class="server-url-input" />
					<button on:click={updateServerUrl} class="generic-button">Save Server URL</button>
				</div>
			{:else if $selectedSetting === 'Clear Cache'}
				<button class="generic-button" on:click={handleClearCache}>Clear Cache</button>
				<!-- Add other miscellaneous options here -->
			{/if}
		</div>
	</div>
</div>

<style lang="postcss">
	.settings-list {
		border-right: 1px solid var(--separator-line-color);
	}

	.settings-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 0.25rem 0.5rem;
		border: none;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.settings-item svg {
		max-height: 1rem;
		max-width: 1rem;
	}

	.settings-item button {
		color: var(--text-color);
	}

	.settings-item:hover {
		background: var(--logo-color);
		color: white;
	}

	.theme-icon {
		display: flex;
		justify-content: center;
		align-items: center;
		background: var(--button-bg-color);
		color: var(--button-text-color);
		border: none;
		border-radius: 0.3rem;
		cursor: pointer;
	}

	.theme-icon:hover {
		background: var(--button-bg-color-hover);
		color: var(--button-text-color-hover);
	}

	.generic-button {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
		border: none;
		border-radius: 5px;
		padding: 5px 10px;
		cursor: pointer;
	}

	.generic-button:hover {
		background: var(--button-bg-color-hover);
		color: var(--button-text-color-hover);
	}

	.api-keys-settings {
		display: flex;
		flex-direction: column;
	}

	.api-key-item {
		display: flex;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.api-key-input {
		padding: 0.5rem;
		border: 1px solid #ccc;
		border-radius: 0.25rem;
		background-color: white;
		color: black;
	}

	.server-settings {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .server-url-input {
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 0.25rem;
        background-color: white;
        color: black;
    }
</style>
