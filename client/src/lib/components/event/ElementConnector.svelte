<!-- src\lib\components\event\ElementConnector.svelte -->

<script lang="ts">
	export let from;
	export let topOffset = 20;
	let bottomOfFrom = 0;
	let container = undefined;
	let topOfContainer = 0;
	$: if (from) {
		bottomOfFrom = from.getBoundingClientRect().bottom;
	}
	$: if (container) {
		topOfContainer = container.getBoundingClientRect().top;
	}
	// when the window is resized, recalculate the positions
	window.addEventListener('resize', () => {
		if (from) {
			bottomOfFrom = from.getBoundingClientRect().bottom;
		}
		if (container) {
			topOfContainer = container.getBoundingClientRect().top;
		}
	});
	setInterval(() => {
		if (from) {
			bottomOfFrom = from.getBoundingClientRect().bottom;
		}
		if (container) {
			topOfContainer = container.getBoundingClientRect().top;
		}
	}, 2000);
</script>

<div class={$$props.class || ``} bind:this={container}>
	<div
		class="
            connector
        "
		style="
            border-bottom-left-radius: 1rem;
            height: {topOfContainer - bottomOfFrom + topOffset}px;
            margin-top: -{topOfContainer - bottomOfFrom}px;
        "
	></div>
	<slot />
</div>

<style>
	.connector {
		margin-left: -20px;
		width: 20px;
		z-index: 1000 !important;
		position: absolute;

		border-left: 2px solid var(--event-card-connector-color);
		border-bottom: 2px solid var(--event-card-connector-color);

		margin-left: -20px !important;
		/* color: white !important; */
	}
</style>
