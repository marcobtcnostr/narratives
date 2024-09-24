<!-- src\lib\components\cards\InfoExpandCard.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';

	import InfoIcon from '$lib/components/icons/InfoFillIcon.svelte';
	import ExpandIcon from '$lib/components/icons/ArrowsAngleExpandIcon.svelte';

	// Props for custom content
	export let title = '';
	export let content = 'Default content...';
	export let header = '';
	export let footer = '';
	export let info = 'Info not available';

	let showInfo = false;
	let expandCard = false;

	onMount(() => {
		// Component mounted
	});

	function toggleInfo() {
		showInfo = !showInfo;
	}

	function toggleExpand() {
		expandCard = !expandCard;
	}
</script>

<div class="card {expandCard ? 'fullscreen' : ''}">
	<div class="card-header">
		<div class="card-header-info">
			<button on:click={toggleInfo} class="card-header-info-button">
				<InfoIcon />
			</button>

			{#if showInfo}
				<div class="info-text">
					{info}
				</div>
			{/if}
		</div>

		<div class="card-header-title">
			{#if header}
				{header}
			{/if}
		</div>

		<div class="card-header-expand">
			<button on:click={toggleExpand} class="card-header-expand-button">
				<ExpandIcon />
			</button>
		</div>
	</div>

	<div class="card-body">
		{#if title}
			<h5 class="card-title">{title}</h5>
		{/if}
		<p class="card-text">{content}</p>
	</div>
	{#if footer}
		<div class="card-footer">
			{footer}
		</div>
	{/if}
</div>

<style>
	.card {
		/* box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); */
		box-shadow:
			0 1px 2px 0 rgba(0, 0, 0, 0.2),
			0 3px 10px 0 rgba(0, 0, 0, 0.19);
		transition: 0.3s;
		border-radius: 5px; /* 5px rounded corners */
	}

	.card:hover {
        border-color: black;
		box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
	}

	.card-body {
		padding: 5px 10px;
	}

	.card-header {
		display: flex; /* Use flexbox */
		align-items: center; /* Align vertically */
		justify-content: space-between; /* Distribute space */
		padding: 5px 10px;
		background: #f1f1f1;
		border-radius: 5px 5px 0 0; /* Rounded corner for the header */
        height: 20px;
	}

	.card-header-info,
	.card-header-expand {
		display: flex; /* Use flexbox */
		align-items: center; /* Align vertically */
		justify-content: center; /* Center horizontally */
		width: 27.5px;
	}

	.card-header-info-button,
	.card-header-expand-button {
		display: flex; /* Use flexbox */
		align-items: center; /* Align vertically */
		justify-content: space-between; /* Distribute space */
		background: none;
		border: none;
		cursor: pointer;
	}

    .card-header-info-button:hover,
	.card-header-expand-button:hover {
        background-color: black;
        color: white;
        border-radius: 5px;
		box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
	}

	.info-text {
		position: absolute;
		width: 300px;
		background-color: #f0b27a;
		padding: 5px 10px;
		border-radius: 5px;
		z-index: 1000;
		top: 0%;
		/* bottom: 0%; */
		left: 40px;
		right: 0%;
		transform: translateX(0%);
	}

	.card-header-title {
		flex-grow: 1;
		text-align: center;
	}

	.card-footer {
		padding: 5px 10px;
		background: #f1f1f1;
		border-radius: 0 0 5px 5px; /* Rounded corner for the footer */
	}

	.card-title {
		margin-bottom: 15px;
	}

	.fullscreen {
		position: fixed; /* Position fixed to the viewport */
		top: 0;
		right: 0;
		bottom: 0;
		left: 0;
		width: 100vw; /* Full viewport width */
		height: 100vh; /* Full viewport height */
		z-index: 1000; /* Ensure it's above other content */
		margin: 0; /* Remove margins */
		box-shadow: none; /* Optional: remove shadow */
		border-radius: 0; /* Optional: remove rounded corners */
		overflow: auto; /* Enable scroll if content is larger than the screen */
	}
</style>
