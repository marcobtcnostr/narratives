<!-- src\lib\components\event\EventCardDropdownMenu.svelte -->
<script lang="ts">
	// import { copyToClipboard } from "../utils";
	import { Copy, Link, MoreVertical, Trash } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	export async function copyToClipboard(textToCopy) {
		try {
			await navigator.clipboard.writeText(textToCopy);
		} catch (err) {
			console.error('Failed to copy: ', err);
		}
	}

	const dispatch = createEventDispatcher();
	export let event;
	export let open = false;
	export let enableDelete = false;

	let copiedEventId = false;
	let copiedEventJSON = false;

	function copyId(e) {
		e.stopPropagation();
		copyToClipboard(event.encode());
		copiedEventId = true;
		setTimeout(() => {
			copiedEventId = false;
		}, 1000);
	}

	function copyJSON(e) {
		e.stopPropagation();
		copyToClipboard(JSON.stringify(event.rawEvent()));
		copiedEventJSON = true;
		setTimeout(() => {
			copiedEventJSON = false;
		}, 1000);
	}
</script>

<div
	class="event-card--dropdown-button {open
		? 'event-card--dropdown-button---opened'
		: 'event-card--dropdown-button---closed'}"
>
	<button
		on:click={() => {
			open = !open;
		}}
		class="dropdown-toggle-button"
	>
		<MoreVertical size="16" />
	</button>

	{#if open}
		<ul class="event-card--dropdown-menu">
			<slot />
			<li>
				<button on:click={() => dispatch('open')} class="dropdown-item">
					<Link size="16" />
					Open Link
				</button>
			</li>
			<li>
				<button on:click={copyId} class="dropdown-item">
					<Copy size="16" />
					<span>{copiedEventId ? 'Copied!' : 'Copy ID'}</span>
				</button>
			</li>
			<li>
				<button on:click={copyJSON} class="dropdown-item">
					<Copy size="16" />
					<span>{copiedEventJSON ? 'Copied!' : 'Copy Event JSON'}</span>
				</button>
			</li>
			{#if enableDelete}
				<li>
					<button on:click={() => dispatch('delete')} class="dropdown-item">
						<Trash size="16" />
						Delete
					</button>
				</li>
			{/if}
		</ul>
	{/if}
</div>

<style>
	.event-card--dropdown-button {
		position: relative;
		display: inline-block;
	}

	.dropdown-toggle-button {
		@apply w-6 h-6 xs:w-6 xs:h-6 sm:w-8 sm:h-8 md:w-8 md:h-8 lg:w-8 lg:h-8;
		/* background-color: var(--button-bg-color); */
		/* box-shadow: var(--box-shadow); */
		color: var(--text-color);
		border: none;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		transition: background-color 0.3s;
	}

	.dropdown-toggle-button:hover,
	.dropdown-toggle-button:focus {
		background-color: var(--text-color);
		/* box-shadow: var(--box-shadow); */
		color: var(--text-color-hover);
	}

	ul {
		position: absolute;
		top: 100%;
		right: 0;
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		border-radius: 4px;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		z-index: 1000;
		padding: 5px 0;
		margin: 2px 0 0;
	}

	.dropdown-item {
		background-color: var(--button-bg-color);
		color: var(--button-text-color);
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 16px;
		cursor: pointer;
		white-space: nowrap;
	}

	.dropdown-item:hover {
		background-color: var(--button-bg-color-hover);
		color: var(--button-text-color-hover);
	}

	.event-card--dropdown-button---opened .dropdown-toggle-button {
		background-color: var(--button-bg-color);
		box-shadow: var(--box-shadow);
		color: var(--button-text-color);
	}
</style>
